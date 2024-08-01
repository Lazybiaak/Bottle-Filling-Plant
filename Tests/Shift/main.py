import multiprocessing
import time
import filled
Station = ['N', 'N', 'N', 'N', 'N', 'N']

def rotate_station(shared_station):
    shared_station[:] = shared_station[-1:] + shared_station[:-1]  # Rotate the list

def first_sixth(shared_station):
    if is_bottle_available(): #check bottle has arrived
        shared_station[0] = 'E' #Empty bottle in first station

def second_sixth(shared_station):
    if bottle_filled():
        shared_station[1] = 'F'

def third_sixth(shared_station):
    dist=filled.distance()
    if dist <= 10:
        shared_station[2] = 'I'
    else if dist

def fourth_sixth(shared_station):
    shared_station[3] = 'C'

def fifth_sixth(shared_station):
    shared_station[4] = 'P'

def sixth_sixth(shared_station):
    shared_station[5] = 'N'

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_station = manager.list(Station)  # Create a shared list

    # Creating separate processes for each script function
    process1 = multiprocessing.Process(target=first_sixth, args=(shared_station,))
    process2 = multiprocessing.Process(target=second_sixth, args=(shared_station,))
    process3 = multiprocessing.Process(target=third_sixth, args=(shared_station,))
    process4 = multiprocessing.Process(target=fourth_sixth, args=(shared_station,))
    process5 = multiprocessing.Process(target=fifth_sixth, args=(shared_station,))
    process6 = multiprocessing.Process(target=sixth_sixth, args=(shared_station,))

    # Starting the processes
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()

    # Joining the processes to ensure they complete before exiting
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    process6.join()

    rotate_station(shared_station)  # Rotate the list after all modifications
    print(list(shared_station))  # Convert to regular list for printing