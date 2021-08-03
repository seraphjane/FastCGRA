import os
import sys
import random
import datetime as dt
import subprocess as sp

if __name__ == "__main__": 
    assert len(sys.argv) >= 5

    fileRRG    = sys.argv[1]
    fileFUs    = sys.argv[2]
    fileDFG    = sys.argv[3]
    fileCompat = sys.argv[4]
    numThreads = int(sys.argv[5]) if len(sys.argv) > 5 else 4

    processes = []
    pids = []
    times = []
    for idx in range(numThreads):
        seed = random.randint(0, 1024 * 1024 * 1024)
        processes.append(sp.Popen(["./placeraw", fileRRG, fileFUs, fileDFG, fileCompat, str(seed)], stdout=sp.DEVNULL, stderr=sp.DEVNULL))
        pids.append(processes[idx].pid)
        times.append(dt.datetime.now())
    
    finished = False
    countQuited = 0
    while not finished and countQuited < numThreads: 
        for idx in range(numThreads):
            if not processes[idx].poll() is None: 
                countQuited += 1
                if processes[idx].poll() == 0: 
                    finished = True
                    time = dt.datetime.now() - times[idx]
                    print("Time:", str((time.seconds + time.microseconds / 1000000)), 's')
                    break
    
    for idx in range(numThreads):
        if processes[idx].poll() is None:  
            processes[idx].kill()

    if not finished: 
        print("ALL FAILED")



