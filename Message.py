#!/usr/bin/python
#encoding utf-8

import multiprocessing
import os
import time,datetime


class MyProcess:

    def __init__(self, myid, num, pipe, leader = -1):
        self.myid = myid
        self.num = num 
        self.leader = leader
        self.pipe = pipe
        self.AllPid = []

    def Write(self,pipe):
        pipe.send(self.pid)
        
    def read(self,pipe):
        now  = pipe.recv()
        #print(now)
        self.AllPid.append(now)
        #print(self.AllPid)

    def PrintId(self):
        print('My pId is %d , leader is %d' % (self.pid , self.leader))

    def GetPid(self):
        return os.getpid()

    def GetAllProcess(self, AllProcess):
        self.AllProcess = AllProcess 

    def BroadCast(self):
        for i in range(self.num):
            bd = multiprocessing.Process(target = self.Write,args=(self.pipe[self.myid][i][0],))
            bd.start()
            bd.join()

    def Running(self):
        self.pid = self.GetPid()
        self.BroadCast()
        bds = []
        for i in range(self.num):
            bdget = multiprocessing.Process(target=self.read,args = (self.pipe[i][self.myid][1],))
            bds.append(bdget)
            bdget.start()

        for i in range(len(bds)):
            bds[i].join()

        print('My Pid is %d , BroadCast is ok.' % self.pid)
        print (self.AllPid)


        while True:
            if self.leader == self.pid:
                pass
            elif self.leader == -1:
                self.Election()
            elif self.check(self.leader) == False:
                self.Electon()
            self.PrintId()
            time.sleep(1)
    
    def HeartBeat(self):
        for i in range(self.num):
            heartbeat = multiprocessing.Process(target = self.heart,args = (pipe[self.myid][i]), )
            pass
    
    def message(slef, message_from, message_to, mess):
        msg = [] 
        self.pipe.send(mess)
        
    def Election(self):
#        if self.myid == self.num - 1:
#            pass
#        else:
            for i in range (self.num):
                if self.num < i:
                    pass
                else:
                    pass

def Init(ProcessNum):
    pass

def Main(ProcessNum):
    
    all_process = []
    pipe = []
    Running_Process = []
    AllProcesses = []
    
    for i in range(ProcessNum):
        nowpipe = []
        for j in range(ProcessNum):
            nowpipe.append(multiprocessing.Pipe())
        pipe.append(nowpipe)
    
    for i in range (ProcessNum):
        all_process.append(MyProcess(i, ProcessNum, pipe))
        p = multiprocessing.Process(target = all_process[i].Running,args = ())
#        NowPid = os.getpid(p)
#        AllProcesses.append(NowPid)
        Running_Process.append(p)
    
#    AllProcesses.sort()  

    for i in range (ProcessNum):
        Running_Process[i].start() 

    for i in range (ProcessNum):
        Running_Process[i].join() 

#        all_process[i].PrintId()

if __name__ == '__main__':
    ProcessNum = 4
    Main(ProcessNum)
