import urllib.request
import threading
import sys
import time

originalString = None
startTime = None
endTime = None

class WorkerThread(threading.Thread):
    def __init__(self, threadID, address, hash, range):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.address = address
        self.hash = hash
        self.range = range
    def run(self):
        global originalString, endTime
        #print("Starting worker for range", self.range)
        if (originalString is None):
            result = urllib.request.urlopen("http://%s/%s/%s" % (self.address, self.hash, self.range)).read().decode('ASCII')
            if (result not in ('Invalid input', 'Not found')):
                endTime = round(time.time() * 1000)
                originalString = result


def loadWorkerList(filename):
    with open(filename) as file:
        return [line.rstrip() for line in file.readlines()]
    return None

def crackHash(hash, workersCount):
    global startTime

    workers = loadWorkerList("./worker_list.txt")
    
    if (len(hash) != 32):
        return "Invalid hash"

    if (len(workers) < workersCount):
        return "Not enough workers"
    
    threads = []

    rangeStart = 'a'
    rangeEnd = chr(min(ord('a') + int(26 / workersCount) - 1, ord('z')))
    for i in range(workersCount):
        #print("worker", i + 1, "range is from", rangeStart, "to", rangeEnd)

        threads.append(WorkerThread(i, workers[i], hash, rangeStart + rangeEnd))

        rangeStart = chr(ord(rangeStart) + int(26 / workersCount))
        rangeStart = chr(min(ord(rangeStart), ord('z')))
        if (i == workersCount - 2):
            rangeEnd = 'z'
        else:
            rangeEnd = chr(ord(rangeEnd) + int(26 / workersCount))
            rangeEnd = chr(min(ord(rangeEnd), ord('z')))

    startTime = round(time.time() * 1000)
    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("Invalid number of parameters")
    else:
        hash = sys.argv[1]
        workersCount = int(sys.argv[2])

        crackHash(hash, workersCount)
        print('Not found' if originalString is None else originalString)
        print((endTime - startTime) if originalString is not None else 0)