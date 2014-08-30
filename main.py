from JobScheduler import JobScheduler
from Communicator import Communicator
import sys
import getopt
from config import DEFAULT_CMD_ARGS
import Logging


def readCmdArgs():

    numSeg = DEFAULT_CMD_ARGS["numSegs"]
    logLevel = DEFAULT_CMD_ARGS["logLevel"]
    onlyCp = DEFAULT_CMD_ARGS["onlyCp"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:l:",
                                   ["num_seg", "log_level", "only_cp"])
    except geopt.GetoptError:
        print sys.argv[0] + ' -s <number of segments>'
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print """mpiexec -n <num of processes> python
                    <main file>.py -s <number of segemnts>
                    -l <(d)ebug,(i)nfo,(e)roor,(w)arning,(c)ritical>"""
            sys.exit()

        elif opt in ("-s", "--num_seg"):
            numSeg = int(arg)
            initiator = int(arg)-1

        elif opt in ('-l', "--log_level"):

            levels = dict((('d', 'debug'), ('i', 'info'),
                           ('w', 'warning'), ('e', 'error'),
                           ('c', 'critical')))

            if arg in levels.keys() + ("--"+x for x in levels.values()):
                logLevel = levels.get(arg, arg.replace("--", ""))

            else:
                print "Unknown log level (-l, --log_level)"
                print "Setting it to ", DEFAULT_CMD_ARGS["logLevel"]

        elif opt == '--only_cp':
            onlyCp = True

        else:
            print "unknown symbol -" + opt
            print "Skipping -" + opt + " " + arg

    return numSeg, logLevel, onlyCp

numSegs, logLevel, onlyCp = readCmdArgs()

Logging.level = logLevel
Logging.onlyCp = onlyCp

# set up the distributed environment
environment = Communicator(numSegs)

processId = environment.getMyId()
initiator = environment.totalProc - 1


procJobScheduler = JobScheduler(environment)
if processId == initiator:
    procJobScheduler.runMicroDownload()
else:
    procJobScheduler.runMicroNC()

environment.setUpBarrier()
