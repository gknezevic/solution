"""This module is main module for contestant's solution."""
from hackathon.solution.bess import preventBessOverload
from hackathon.solution.constants import PERIOD_WITHOUT_POWER_DOWN, MINIMAL_BATTERY_POWER_FOR_LOAD_1
from hackathon.solution.regularScenarios import handleRegularScenarios, shutdownLoadIfPowerIsExpensive
from hackathon.solution.statuses import saveReceivedStatus, saveSentStatus
from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
import sys

listOfReceivedStatuses = []
listOfSentStatuses = []

minBuyingCosts = []
maxBuyingCosts = []
sellingCosts = []

lastPowerDown = []

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    if len(lastPowerDown) == 0:
        lastPowerDown.append(-1000)

    MIN_ENERGY_FOR_BATTERY = MINIMAL_BATTERY_POWER_FOR_LOAD_1

    if msg.grid_status == False:
        lastPowerDown[0] = msg.id
    else:
        if msg.id - lastPowerDown[0] < PERIOD_WITHOUT_POWER_DOWN:
            MIN_ENERGY_FOR_BATTERY = 0.11

    if len(minBuyingCosts) == 0:
        minBuyingCosts.append(msg.buying_price)
        maxBuyingCosts.append(msg.buying_price)
        sellingCosts.append(msg.selling_price)
    else:
        if minBuyingCosts[0] > msg.buying_price:
            minBuyingCosts[0] = msg.buying_price

        if maxBuyingCosts[0] < msg.buying_price:
            maxBuyingCosts[0] = msg.buying_price

        if sellingCosts[0] < msg.selling_price:
            sellingCosts[0] = msg.selling_price

    # Save received status from framework
    saveReceivedStatus(msg, listOfReceivedStatuses)

    # set default output message witch should be changed
    batteryUsing = 0.0
    newOutput = ResultsMessage(msg, True, True, True, batteryUsing, PVMode.ON)
    shutdownLoadIfPowerIsExpensive(listOfReceivedStatuses[0], newOutput)

    defaultOutputStatus = ResultsMessage(msg, True, True, True, 0.0, PVMode.ON) if len(listOfSentStatuses) == 0 else listOfSentStatuses[0]
    # Prevent battery overload
    if msg.bessOverload :
        preventBessOverload(listOfReceivedStatuses[0], defaultOutputStatus, newOutput, minBuyingCosts[0], maxBuyingCosts[0],
                            MIN_ENERGY_FOR_BATTERY)
    else:
        handleRegularScenarios(listOfReceivedStatuses[0], defaultOutputStatus, newOutput, minBuyingCosts[0], maxBuyingCosts[0],
                               MIN_ENERGY_FOR_BATTERY)


    saveSentStatus(newOutput, listOfSentStatuses)

    if msg.id - lastPowerDown[0] > PERIOD_WITHOUT_POWER_DOWN and msg.bessSOC * 10.0 < MINIMAL_BATTERY_POWER_FOR_LOAD_1:
        newOutput.power_reference = -6.0

    return newOutput;

def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
