"""This module is main module for contestant's solution."""
from hackathon.solution.bess import preventBessOverload
from hackathon.solution.regularScenarios import handleRegularScenarios
from hackathon.solution.statuses import saveReceivedStatus, saveSentStatus
from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
import sys

listOfReceivedStatuses = []
listOfSentStatuses = []

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    print("selling price: " + str(msg.selling_price))
    print("buying price: " + str(msg.buying_price))

    # Save received status from framework
    saveReceivedStatus(msg, listOfReceivedStatuses)

    # set default output message witch should be changed
    batteryUsing = 0.0 if len(listOfSentStatuses) == 0 else listOfSentStatuses[0].power_reference
    newOutput = ResultsMessage(msg, True, True, True, batteryUsing, PVMode.ON)

    defaultOutputStatus = ResultsMessage(msg, True, True, True, 0.0, PVMode.ON) if len(listOfSentStatuses) == 0 else listOfSentStatuses[0]
    # Prevent battery overload
    if msg.bessOverload :
        preventBessOverload(listOfReceivedStatuses[0], defaultOutputStatus, newOutput)
    else:
        handleRegularScenarios(listOfReceivedStatuses[0], defaultOutputStatus, newOutput)

    saveSentStatus(newOutput, listOfSentStatuses)

    return newOutput;

    # Dummy result is returned in every cycle here
    #return ResultsMessage(data_msg=msg,
    #                      load_one=True,
    #                      load_two=True,
    #                      load_three=True,
    #                      power_reference=0.0,
    #                      pv_mode=PVMode.ON)



def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
