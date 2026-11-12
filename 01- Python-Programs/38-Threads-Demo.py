import threading
import time

def task_one():
    print("Task-1 Started")
    time.sleep(3)
    print("Task-1 Completed")

def task_two():
    print("Task-2 Started")
    time.sleep(2)
    print("Task-2 Completed")

t1 = threading.Thread(target=task_one)
t2 = threading.Thread(target=task_two)

#t1.start()
#t2.start()
##########################################

class MyThread(threading.Thread):

    # Method Overriding
    def run(self):
        print("Run() method started..")
        print("Thread Name :", threading.current_thread().name)

t3 = MyThread()
t4 = MyThread()


##t3.start()
###t4.start()

##################################################

def download_file():
    print("Download file started..")
    time.sleep(3)
    print("Download completed")


t5 = threading.Thread(target=download_file)
##t5.start()
##t5.join()

#print("Read data from downloaded file...")


##################################################

def process_data():
    time.sleep(3)

thread = threading.Thread(target=process_data)

thread.start()
print(thread.is_alive())

thread.join()

print(thread.is_alive())

##################################################


print("Current Thread:", threading.current_thread())
print("Thread Name:", threading.current_thread().name)
print("Thread Identifier:", threading.current_thread().ident)
print("Active Thread Count:", threading.active_count())

##################################################














