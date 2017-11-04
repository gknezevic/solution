from hackathon.utils.utils import DataMessage, ResultsMessage


def handleRegularScenarios(currentInput:DataMessage, previousOutput:ResultsMessage, newOutput:ResultsMessage):
    if currentInput.grid_status == False:
        if currentInput.bessSOC * 10 + currentInput.solar_production <= currentInput.current_load * 0.2:
            newOutput.load_two = False
            newOutput.load_three = False
        elif currentInput.bessSOC * 10 + currentInput.solar_production <= currentInput.current_load * 0.7:
            newOutput.load_three = False

    else:
        Pbess = currentInput.mainGridPower + currentInput.solar_production - currentInput.current_load
        newOutput.power_reference = Pbess * (-1)