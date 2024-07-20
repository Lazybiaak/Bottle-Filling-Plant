print("This is where parallel processing is tested")

import multiprocessing
import subprocess
def run_script(script_name):
    subprocess.run(["python", script_name])
if __name__ == "__main__":
    scripts = ["script1.py", "script2.py", "script3.py"]
    processes = []

    for script in scripts:
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
