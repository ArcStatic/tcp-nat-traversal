import socket
import sys
import thread
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind((sys.argv[1], int(sys.argv[2])))

clients = []
client_own_info = []



def session(c, addr):
    print("Client thread started.")
    while True:
        print("Thread for %s responding" % str(addr))
        #c.send("Your addr:port pair is: %s" % str(addr))
        #ie. if there is another client waiting, send details to connected client
        if len(clients) > 1:
            for i in range(len(clients)):
                if clients[i] != addr:
                    info = str(str(clients[i])[2:-1] + client_own_info[i])
                    c.send(info)
            c.close()
            print("Client thread terminating...")
            thread.exit()
        time.sleep(3)

def monitor(s):
    s.listen(5)
    while True:
        c, addr = s.accept()
        print("Connection from %s" % str(addr))
        clients.append(addr)
        client_private = c.recv(1024)
        client_own_info.append(client_private)
        print(client_own_info)
        try:
            client_thread = threading.Thread(target=session, args=(c,addr))
            client_thread.start()
            #thread.start_new_thread(session(c, addr))
        except:
            print("Error starting client thread for %s." % str(addr))



monitor(s)

