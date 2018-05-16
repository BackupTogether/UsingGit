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
        try:
            now  = pipe.recv()
        except:
            pass
        #print(now)
        #self.AllPid.append(now)
        #print(self.AllPid)

    def PrintId(self):
        print('My pId is %d , leader is %d' % (self.pid , self.leader))

    def GetPid(self):
        return os.getpid()

    def GetAllProcess(self, AllProcess):
        self.AllProcess = AllProcess 

    def BroadCast(self):
        for i in range(self.num):
            #bd = multiprocessing.Process(target = self.Write,args=(self.pipe[self.myid][i][0],))
            #bd.start()
            #bd.join()
            self.pipe[self.myid][i][0].send(['BroadCast',self.pid])

    def Election(self):
        print(self.pid,'Election start')
        for i in range(self.num):
            try:
                self.pipe[self.myid][i][0].send("quest")
            except:
                pass

        ok = True

        for i in range(self.num):
            try:
                now = None
                while self.pipe[i][self.myid][1].poll():
                    now = self.pipe[i][self.myid][1].recv()
                if now != None and self.AllPid[i] > self.pid:
                    ok = False
            except:
                pass
        if ok:
            self.leader = self.pid


    def Running(self):
        self.pid = self.GetPid()
        self.BroadCast()
        bds = []
        for i in range(self.num):
            # bdget = multiprocessing.Process(target=self.read,args = (self.pipe[i][self.myid][1],))
            # bds.append(bdget)
            # bdget.start()
            now  = self.pipe[i][self.myid][1].recv()
            # print("Me:%s, Now: %s" % (self.pid, now))
            if(now[0]== 'BroadCast'):
                self.AllPid.append(now[1])
            # print(self.AllPid)

#        for i in range(len(bds)):
#            bds[i].join()

        print('My Pid is %d , BroadCast is ok.' % self.pid)
        #print('All process listed below:')
        #print (self.AllPid)
        self.AllPid.sort()
        time.sleep(3)

        if self.leader == -1 and self.pid == self.AllPid[-1]:
            self.leader = self.pid
            self.BroadCast()
        while True:
            if self.leader == self.pid:
                self.BroadCast()
            elif self.leader == -1:
                #self.Election()
                try:
                    for i in range(self.num):
                        nowstate = self.pipe[i][self.myid][1].poll()
                        if(nowstate == False):
                            continue
                        else:
                            now = self.pipe[i][self.myid][1].recv()
                            if(now[1] > self.pid):
                                self.leader = now[1]
                except:
                    pass
            else: 
                ok = False
                try:
                    for i in range(5):
                        for j in range(self.num):
                            if self.AllPid[j] == self.leader:
                                nowstate = self.pipe[j][self.myid][1].poll()
                                if nowstate == True:
                                    while self.pipe[j][self.myid][1].poll():
                                        a = self.pipe[j][self.myid][1].recv()
                                    ok = True
                    time.sleep(0.3)
                except:
                    pass
                if not ok:
                    print(self.pid,'start')
                    self.leader = -1
                    self.Election()
                #self.check(self.leader) == False:
                #print(self.pid)
                #self.Electon()
            time.sleep(1)
            try:
                self.PrintId()
            except:
                pass
    
    def HeartBeat(self):
        for i in range(self.num):
            heartbeat = multiprocessing.Process(target = self.heart,args = (pipe[self.myid][i]), )
            pass
    
    def message(self, message_from, message_to, mess):
        msg = [] 
        self.pipe.send(mess)

    def check(self, test_leader):
        for i in range(5):
            for j in range(self.num):
                if self.AllPid[j] == self.leader:
                    nowstate = self.pipe[j][self.myid][1].poll()
                    if nowstate == True:
                        while self.pipe[j][self.myid][1].poll():
                            a = self.pipe[j][self.myid][1].recv()
                        return True
            time.sleep(0.3)
        return False
        

def Init(ProcessNum):
    pass

def Main(ProcessNum):
    
    all_process = []
    pipe = []
    Running_Process = []
    AllProcesses = []
    Pipe_Port = []

    
    for i in range(ProcessNum):
        nowpipe = []
        nowport = []
        for j in range(ProcessNum):
            a,b = multiprocessing.Pipe()
            #nowpipe.append(a,b = multiprocessing.Pipe())
            nowport.append([a,b])
        #pipe.append(nowpipe)
        Pipe_Port.append(nowport)
    
    for i in range (ProcessNum):
        all_process.append(MyProcess(i, ProcessNum, Pipe_Port))
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
