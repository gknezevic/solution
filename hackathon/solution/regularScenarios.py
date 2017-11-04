from hackathon.solution.constants import BATTERY_MAX_OUTPUT_POWER, MINIMAL_BATTERY_POWER_FOR_LOAD_1, \
    MINIMAL_BATTERY_POWER_FOR_LOAD_1_AND_LOAD_2
from hackathon.utils.utils import DataMessage, ResultsMessage


def handleRegularScenarios(currentInput:DataMessage, previousOutput:ResultsMessage, newOutput:ResultsMessage):
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
        if currentInput.bessSOC * 10.0 <= MINIMAL_BATTERY_POWER_FOR_LOAD_1:
            newOutput.power_reference = currentInput.bessSOC * 10.0 - 10.0
        else:
            if currentInput.bessSOC > 0.95:
                newOutput.power_reference = 0.0
            else:
                if currentInput.selling_price >= 1 and currentInput.solar_production > 0:
                    newOutput.power_reference = currentInput.solar_production
                elif (currentInput.solar_production - currentInput.current_load) > 0:
                    newOutput.power_reference = (currentInput.current_load - currentInput.solar_production) * 1.0
                else:
                    newOutput.power_reference = 0.0


