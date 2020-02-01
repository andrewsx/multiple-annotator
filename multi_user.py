import prodigy
from multiprocessing import Process
from time import sleep
from prodigy.recipes.ner import batch_train
import atexit
from pathlib import Path
import datetime as dt
import socket 
import asyncio
ip = socket.gethostbyname(socket.gethostname())
class MultiUser:

    def __init__(self, name, port):
        #self.users_list = users_list
        self.name = name
        self.designated_port = port
        self.processes = []

    def make_prodigies(self, dataset_name, input_data, spacy_model, labels):
        thread = Process(target=self.serve, args=(dataset_name, self.name, self.designated_port, input_data, spacy_model, labels))
        self.processes.append(thread)

        #for coder_info in enumerate(self.users_list):
        #     print(coder_info)
        #     coder_info = coder_info[1]
        #     thread = Process(target=self.serve, args=(dataset_name,
        #                                              coder_info['name'], coder_info['port'], input_data, spacy_model, labels))
            
        #     self.processes.append(thread)

    def serve(self, dataset_name, coder, port, input_data, spacy_model, labels):
        print('Dataset name in DB:', ',', dataset_name, 'Coder:', coder, ',', 'Port #:', port, ',', 'Dataset file input:', ',', input_data, 'Spacy Model:', ',', spacy_model, 'User Labels:', ',', labels)
        prodigy.serve('ner.manual', dataset_name, spacy_model,
                      input_data, None, None, labels, None, host=ip, port=port)


    # def serve(self, dataset_name, coder, port, input_data, spacy_model):
    #     print('Coder:', coder, ',', 'Port #:', port)
    #     prodigy.serve('ner.manual', dataset_name, 'en_core_web_sm',
    #                   'emails_remaining.txt', None, None, ['ADDRESS'], None, host=ip, port=port)

    def start_prodigies(self):
        print("Starting Prodigy processes...")
        for p in self.processes:
            p.start()
            sleep(1)

    def kill_prodigies(self):
        print("Killing Prodigy threads")
        for i in self.processes:
            try:
                i.terminate()
            except AttributeError:
                print("Process {0} doesn't exist?".format(i))
        self.processes = []


