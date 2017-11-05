from hackathon.solution.constants import BATTERY_MAX_OUTPUT_POWER, MINIMAL_BATTERY_POWER_FOR_LOAD_1, \
    MINIMAL_BATTERY_POWER_FOR_LOAD_1_AND_LOAD_2, BATTERY_SELLING_OUTPUT, MAX_BUYING_PRICE
from hackathon.utils.utils import DataMessage, ResultsMessage


def handleRegularScenarios(currentInput:DataMessage, previousOutput:ResultsMessage, newOutput:ResultsMessage, minBuyingPrice, maxBuyingPrice, MIN_ENERGY_FOR_BATTERY):
    if currentInput.grid_status == False:
        if currentInput.bessSOC * 10 + currentInput.solar_production <= MINIMAL_BATTERY_POWER_FOR_LOAD_1:
            newOutput.load_two = False
            newOutput.load_three = False
        elif currentInput.bessSOC * 10 + currentInput.solar_production <= MINIMAL_BATTERY_POWER_FOR_LOAD_1_AND_LOAD_2:
            newOutput.load_three = False

        if currentInput.solar_production + BATTERY_MAX_OUTPUT_POWER < currentInput.current_load:
            newOutput.load_three = False
        if currentInput.solar_production + BATTERY_MAX_OUTPUT_POWER < currentInput.current_load * 0.7:
            newOutput.load_two = False
        if currentInput.solar_production + BATTERY_MAX_OUTPUT_POWER < currentInput.current_load * 0.2:
            newOutput.load_one = False

    else:
        extraEnergy = currentInput.solar_production - predictFutureConsumption(newOutput.load_two, newOutput.load_three,
                                 currentInput.current_load)

        if extraEnergy > 0:
            if currentInput.bessSOC * 10.0 <= 9.9:
                # Charge battery
                newOutput.power_reference = extraEnergy * (-1.0)
            elif currentInput.selling_price > 0:
                newOutput.power_reference = 0.0
            else:
                newOutput.power_reference = 0.0

                if newOutput.load_two == False and newOutput.load_three == False:
                    if extraEnergy + 6 > currentInput.current_load * 0.8:
                        newOutput.load_two = True
                        newOutput.load_three = True
                        if extraEnergy >= currentInput.current_load * 0.8:
                           newOutput.power_reference = 0.0
                        elif currentInput.buying_price == maxBuyingPrice:
                            newOutput.power_reference = currentInput.current_load * 0.8 - extraEnergy
                        else:
                            newOutput.load_two = False
                            newOutput.load_three = False

                elif newOutput.load_two == False:
                    if extraEnergy + 6 > currentInput.current_load * 0.5:
                        newOutput.load_two = True
                        if extraEnergy >= currentInput.current_load * 0.5:
                           newOutput.power_reference = 0.0
                        elif currentInput.buying_price == maxBuyingPrice:
                            newOutput.power_reference = currentInput.current_load * 0.5 - extraEnergy
                        else:
                            newOutput.load_two = False

                elif newOutput.load_three == False:
                    if extraEnergy + 6 > currentInput.current_load * 0.3:
                        newOutput.load_three = True
                        if extraEnergy >= currentInput.current_load * 0.3:
                           newOutput.power_reference = 0.0
                        elif currentInput.buying_price == maxBuyingPrice:
                            newOutput.power_reference = currentInput.current_load * 0.3 - extraEnergy
                        else:
                            newOutput.load_three = False

        else:
            if currentInput.buying_price == minBuyingPrice and currentInput.bessSOC * 10.0 < 9.88:
                newOutput.power_reference = -6.0
            elif currentInput.bessSOC * 10.0 > MIN_ENERGY_FOR_BATTERY:
                if currentInput.buying_price == maxBuyingPrice:
                    newOutput.power_reference = extraEnergy * (-1.0)
            else:
                newOutput.power_reference = 0.0


def shutdownLoadIfPowerIsExpensive(currentInput:DataMessage, newOutput: ResultsMessage):
    if currentInput.buying_price * currentInput.current_load * 0.3/60 > 0.1:
        newOutput.load_three = False
    if currentInput.buying_price * currentInput.current_load * 0.5/60 > 0.4:
        newOutput.load_two = False

def predictFutureConsumption(load2:bool, load3:bool, teorethicalLoad:float):
    intLoad2 = 1 if load2 else 0
    intLoad3 = 1 if load3 else 0
    return teorethicalLoad*0.2 + teorethicalLoad*0.5*intLoad2 + teorethicalLoad*0.3*intLoad3
