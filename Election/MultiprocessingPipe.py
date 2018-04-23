import os
import time
from datetime import datetime
from multiprocessing import Process, Pipe

def f(conn, name):
    conn.send('My process id: %d' % os.getpid())
    for x in xrange(1,5):
        conn.send('[%s] %s process id: %d' % (datetime.now(), name, os.getpid()))
        print('%s says: %s' % (name, conn.recv()))
        time.sleep(3)
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p1 = Process(target=f, args=(child_conn, 'Children'))
    p2 = Process(target=f, args=(parent_conn, 'Parent'))
    p1.start()
    time.sleep(3)
    p2.start()

    p1.join()
    p2.join()



# def info(title):
#     print title
#     print 'module name:', __name__
#     if hasattr(os, 'getppid'):  # only available on Unix
#         print 'parent process:', os.getppid()
#     print 'process id:', os.getpid()

# def f(name):
#     info('function f')
#     print 'hello', name

# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()
#     







