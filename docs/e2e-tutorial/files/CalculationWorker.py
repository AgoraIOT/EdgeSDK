#################################################################
# Agora Digital Solutions Inc.
# ###############################################################
# Copyright 2020 Agora Digital Solutions IncS.

# All rights reserved in Agora Digital Solutions Inc. authored and generated cod
e (including the selection and arrangement of the source code base regardless of
 the authorship of individual files), but not including any copyright interest(s
) owned by a third party related to source code or object code authored or gener
ated by non- Agora Digital Solutions Inc. personnel.
# Any use, disclosure and/or reproduction of source code is prohibited unless in
 compliance with the AGORA SOFTWARE DEVELOPMENT KIT LICENSE AGREEMENT.
#################################################################
from WorkerThread import WorkerThread
from HBM_PythonAppManagerBindings import *
import time, csv, json, random
import logging
#import numpy as np

import os
script_dir = os.path.dirname(__file__)

class CalculationWorker(WorkerThread):
    privateRun = False
    privateBusClient = None
    privateDataOutEndpoint = ""

    def __init__(self):
        WorkerThread.__init__(self)
        self.setName("CalculationWorker")
        self.privateRun = False

        #setup the IOs
        self.privateA = IO_POINT_T()
        self.privateB = IO_POINT_T()
        self.privateC = IO_POINT_T()

        self.privateA.name = "io-a"
        self.privateB.name = "io-b"
        self.privateC.name = "io-c"

        self.privateA.ion_data_type = 8
        self.privateB.ion_data_type = 8
        self.privateC.ion_data_type = 8

        self.privateA.io_id = 1
        self.privateB.io_id = 2
        self.privateC.io_id = 3

        self.sleep_interval = 60
        self.target_device_id = 274

        self.simulator_csv_path = os.path.join(script_dir, "simulated_data.csv")
        #flag to stop csv simulator
        self.csv_stop = False

    def Configure(self, serializer):
        logging.debug("New config received")

    def Initialize(self, name, busClient, dataOutEndpoint):
        logging.debug("Initialize thread CalculationWorker")
        self.privateBusClient = busClient
        self.privateDataOutEndpoint = dataOutEndpoint

    def HandleData(self, serializer):
        logging.debug("handleData thread CalculationWorker")

    def get_message_id(self):
        # Message id shouldn't exceed max(int32)
        return random.randint(0, 2**31-1)

    def run(self):
        logging.debug("running thread CalculationWorker")
        self.privateRun = True
        with open(self.simulator_csv_path, "r") as self.csvfile:
            while(True):
                self.reader = csv.reader(self.csvfile, skipinitialspace=True)
                header_json = {
                    "device": [
                            {
                                    "id": str(self.target_device_id),
                                    "tags": {
                                            # tags is empty now, will be used later
                                    }
                            }
                    ],
                    "header": {
                            "ConfigVersion": 10,
                            "GroupID": "agora",
                            "LandingPoint": "Edge",
                            "MessageID": 1419819207,
                            "MessageType": "IODataReport",
                            "SrcModule": "simulator",
                            "TimeStamp": 14969454514
                    },
                    "timestamp": "2020-05-29T13:20:00Z"
                    }

                self.reader = list(self.reader)
                #store the tags in a list by reading first line of csv file
                self.tags = self.reader.pop(0)
                for row in self.reader:
                    current_json = {}
                    time_now = int(time.time())
                    for coloumn in range(len(self.tags)):
                        current_json.update({
                            self.tags[coloumn]:{
                                "quality_code":0,
                                "timestamp":time_now,
                                "value": float(row[coloumn])
                            }}
                        )
                    #update header json 
                    header_json['device'][0]['tags'] = current_json
                    header_json['header']['MessageID'] = self.get_message_id()
                    header_json['header']['TimeStamp'] = time_now
                    logging.debug(json.dumps(header_json))
                    self.privateBusClient.SendMessage('DataOut',json.dumps(header_json))
                    time.sleep(self.sleep_interval)
                    if self.csv_stop:
                        break      