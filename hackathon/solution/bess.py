from hackathon.solution.constants import BATTERY_MAX_OUTPUT_POWER
from hackathon.utils.utils import ResultsMessage, DataMessage

def preventBessOverload(currentInput:DataMessage, previousOutput:ResultsMessage, newOutput:ResultsMessage) :

    Pbess = currentInput.current_load - currentInput.solar_production - currentInput.mainGridPower
    if Pbess > BATTERY_MAX_OUTPUT_POWER:
        if previousOutput.load_three == True:
            newOutput.load_three = False
            if currentInput.current_load * 0.7 > BATTERY_MAX_OUTPUT_POWER:
                newOutput.load_two = False


    elif currentInput.bessSOC == 0:
        if currentInput.grid_status == False:
            newOutput.power_reference = 0
            if currentInput.solar_production >= currentInput.current_load * 0.2:
                newOutput.load_one = True
            if currentInput.solar_production >= currentInput.current_load * 0.7:
                pass
