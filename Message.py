#!/usr/bin/python
#encoding utf-8

import multiprocessing

class MyProcess:

    def __init__(self,id):
        self.id = id

    def PrintId(self):
        print('My Process_Id is %d' % self.id)

def Main(ProcessNum):
    all_process = []
    
    for i in range (ProcessNum):
        all_process.append(MyProcess(i))
        all_process[i].PrintId()

if __name__ == '__main__':
    ProcessNum = 4
    Main(ProcessNum)
