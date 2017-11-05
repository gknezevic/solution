
def predictFutureConsumption(load2:bool, load3:bool, teorethicalLoad:float):
    intLoad2 = 1 if load2 else 0
    intLoad3 = 1 if load3 else 0
    return teorethicalLoad*0.2 + teorethicalLoad*0.5*intLoad2 + teorethicalLoad*0.3*intLoad3

result = predictFutureConsumption(False, False, 5.0)

print("Result is: " + str(result))
