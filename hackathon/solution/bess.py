from hackathon.solution.constants import BATTERY_MAX_OUTPUT_POWER
from hackathon.solution.regularScenarios import handleRegularScenarios
from hackathon.utils.utils import ResultsMessage, DataMessage

def preventBessOverload(currentInput:DataMessage, previousOutput:ResultsMessage, newOutput:ResultsMessage) :

    Pbess = currentInput.current_load - currentInput.solar_production - currentInput.mainGridPower
    if Pbess > BATTERY_MAX_OUTPUT_POWER:
        if previousOutput.load_three == True:
            newOutput.load_three = False
            if currentInput.current_load * 0.7 > BATTERY_MAX_OUTPUT_POWER:
                newOutput.load_two = False

    # Case when battery is empty
    elif currentInput.bessSOC == 0:
        if currentInput.grid_status == False:
            turn_off_loads(newOutput)
            newOutput.power_reference = 0.0
            availablePower = currentInput.solar_production
            if currentInput.solar_production >= currentInput.current_load * 0.2:
                newOutput.load_one = True
                availablePower = currentInput.solar_production - currentInput.current_load * 0.2
            if currentInput.solar_production >= currentInput.current_load * 0.7:
                newOutput.load_two = True
                availablePower = currentInput.solar_production - currentInput.current_load * 0.7
            newOutput.power_reference = availablePower * (-1)
        else:
            turn_off_loads(newOutput)
            newOutput.power_reference = 0.0
            availablePower = currentInput.solar_production
            if currentInput.solar_production + currentInput.mainGridPower >= currentInput.current_load * 0.2:
                newOutput.load_one = True
                availablePower = currentInput.solar_production + currentInput.mainGridPower - currentInput.current_load * 0.2
            if currentInput.solar_production + currentInput.mainGridPower >= currentInput.current_load * 0.7:
                newOutput.load_two = True
                availablePower = currentInput.solar_production + currentInput.mainGridPower - currentInput.current_load * 0.7
            if currentInput.solar_production + currentInput.mainGridPower >= currentInput.current_load:
                newOutput.load_three = True
                availablePower = currentInput.solar_production + currentInput.mainGridPower - currentInput.current_load
            newOutput.power_reference = availablePower * (-1)

    # Case when battery is full
    elif currentInput.bessSOC == 1:
        handleRegularScenarios(currentInput, previousOutput, newOutput)
        if newOutput.power_reference > 0.0:
            newOutput.power_reference = 0.0

def turn_off_loads(newOutput):
    newOutput.load_one = False
    newOutput.load_two = False
    newOutput.load_three = False

def turn_on_loads(newOutput):
    newOutput.load_one = True
    newOutput.load_two = True
    newOutput.load_three = True