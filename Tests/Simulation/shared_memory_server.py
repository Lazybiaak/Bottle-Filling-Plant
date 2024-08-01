import multiprocessing
from multiprocessing.managers import BaseManager

def create_shared_station():
    manager = multiprocessing.Manager()
    return manager.list(['N', 'N', 'N', 'N', 'N', 'N'])

class SharedMemoryManager(BaseManager):
    pass

if __name__ == "__main__":
    SharedMemoryManager.register('get_station', callable=create_shared_station)
    manager = SharedMemoryManager(address=('', 50000), authkey=b'secret')
    server = manager.get_server()
    print("Shared memory server is running...")
    server.serve_forever()
