import time
def calculateTime():
    start_time = time.time()
    #插入你需要测量的函数在下面

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")