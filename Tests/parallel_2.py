import multiprocessing
import time

def script1():
    for i in range(5):
        print("Hello from Script 1")
        time.sleep(1)
    
def script2():
    for i in range(5):
        print("Hello from Script 2")
        time.sleep(0.5)

def script3():
    for i in range(5):
        print("Hello from Script 3")
        time.sleep(0.75)

if __name__ == "__main__":
    # Creating separate processes for each script function
    process1 = multiprocessing.Process(target=script1)
    process2 = multiprocessing.Process(target=script2)
    process3 = multiprocessing.Process(target=script3)

    # Starting the processes
    process1.start()
    process2.start()
    process3.start()

    # Joining the processes to ensure they complete before exiting
    process1.join()
    process2.join()
    process3.join()
