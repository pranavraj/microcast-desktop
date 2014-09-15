# contains information about the segments
# to be used only by the MicroDownload.py

import time
import random
import urllib
import json

class SegmentHandler:

    def __init__(self, numSegs):
        self.metadata = None
        self.numSegs = numSegs
        self.segmentAssignList = []
        self.downloadedList = []
        """
            self.metadata fields
            ~~~~~~~~~~~~~~~~~~~~~~
            {
                numSegments :  N,
                1 : {
                        segmentDownloadtime: K0,
                        segmentFrom : K1,
                        segmentTo : K2
                    }
                .......
            }
        """

    def downloadMetadata(self, url , videoName ):
        # Static data as of now
        url = url + urllib.urlencode({'init':'True','file': 'music.mp4'})
        meta = json.loads(urllib.urlopen(url).read())

        
        self.metadata = {"numSegments": len(meta["Segments"])}
        self.metadata["size"] = meta["size"]

        for i in range(self.numSegs):
            for i in meta["Segments"]:
                self.metadata[i] = {"segmentFrom": meta["Segments"]}
                self.segmentAssignList.append(False)
                self.downloadedList.append(False)

    def getMetadata(self, segmentId):
        return self.metadata[segmentId]

    def allAssigned(self):
        return all(self.segmentAssignList)

    def allDownloaded(self):
        return all(self.downloadedList)

    def isDownloaded(self, segmentId):
        self.downloadedList[segmentId] = True

    def assignSegment(self, segmentId):
        self.segmentAssignList[segmentId] = True

    def unassignSegment(self, segmentId):
        self.segmentAssignList[segmentId] = False

    def getNextUnassigned(self):
        # used only by microDownload
        if not self.allAssigned():
            return random.choice(
                [i for i, x in enumerate(self.segmentAssignList) if not x])
        return -1
