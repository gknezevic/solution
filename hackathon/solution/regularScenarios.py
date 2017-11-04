from hackathon.solution.constants import BATTERY_MAX_OUTPUT_POWER
from hackathon.utils.utils import DataMessage, ResultsMessage


def handleRegularScenarios(currentInput:DataMessage, previousOutput:ResultsMessage, newOutput:ResultsMessage):
    if currentInput.grid_status == False:
        if currentInput.bessSOC * 10 + currentInput.solar_production <= currentInput.current_load * 0.2:
            newOutput.load_two = False
            newOutput.load_three = False
            print("left batery less than: " + str(currentInput.current_load * 0.2))
        elif currentInput.bessSOC * 10 + currentInput.solar_production <= currentInput.current_load * 0.7:
            newOutput.load_three = False

        if currentInput.solar_production + BATTERY_MAX_OUTPUT_POWER < currentInput.current_load:
            newOutput.load_three = False
        if currentInput.solar_production + BATTERY_MAX_OUTPUT_POWER < currentInput.current_load * 0.7:
            newOutput.load_two = False
        if currentInput.solar_production + BATTERY_MAX_OUTPUT_POWER < currentInput.current_load * 0.2:
            newOutput.load_one = False

    else:
        availablePower = 0.0
        if currentInput.bessSOC * 10 + currentInput.solar_production <= currentInput.current_load * 0.2:
            availablePower = 0.0
        else:
            availablePower = currentInput.current_load - currentInput.solar_production

        newOutput.power_reference = 0.0