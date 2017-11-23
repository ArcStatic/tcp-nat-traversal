import socket
import sys
import threading
import time

addr = sys.argv[1]
port = int(sys.argv[2])

own_addr = sys.argv[3]
own_port = int(sys.argv[4])

a = ""

s_stun = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#set socket to be able to be reassigned to the same address:port without timeout
s_stun.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s_stun.bind((own_addr, own_port))
#s_stun.bind(("192.168.0.66", 22022))
#s_stun.bind(("172.30.154.232", 22022))

s_stun.connect((addr, port))
own_info = "', " + own_addr + "', " + str(own_port)
s_stun.send(own_info)
print("Connected.")
while True:
    try:
        msg = s_stun.recv(1024)
        s_stun.close()
        print(msg)
        msg = msg.split("', ")
        print(msg)
        peer_addr = msg[0]
        peer_port = int(msg[1])
        peer_private_addr = msg[0]
        peer_private_port = int(msg[1])
        print("peer_addr: %s" % msg[0])
        print("peer_port: %s" % msg[1])
        print("public_addr: %s" % msg[2])
        print("public_port: %s\n" % msg[3])
        break
    except:
        break


s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s_listen.settimeout(5)
s_listen.bind((own_addr, own_port))

s_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_peer.settimeout(5)
s_peer.bind((own_addr, own_port))

s_peer_private = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_peer_private.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_peer_private.settimeout(5)
s_peer_private.bind((own_addr, own_port))

for i in range(2):
    try:
        s_peer.connect((peer_addr, peer_port))
        s_peer_private.connect((peer_private_addr, peer_private_port))
    except:
        #s_peer.close()
        pass

def listening_thread(s_listen, a):
    s_listen.listen(2)
    while True:
        #try:
        c, addr = s_listen.accept()
        print("Peer connection received: %s" % str(addr))
        #except:
            #pass
        
def connection_thread(s_peer, peer_addr, peer_port):
    while True:
        try:
            print("Attempting peer connection...")
            s_peer.connect((peer_addr, peer_port))
            time.sleep(3)
        except Exception as e:
            print(e)
            #s_peer.close()
            time.sleep(3)

def connection_private_thread(s_peer_private, peer_private_addr, peer_private_port):
    while True:
        try:
            print("Attempting peer connection on private endpoint...")
            s_peer_private.connect((peer_private_addr, peer_private_port))
            time.sleep(3)
        except Exception as e:
            print(e)
            #s_peer_private.close()
            time.sleep(3)
    
listen_thread = threading.Thread(target=listening_thread, args=(s_listen, a))
peer_thread = threading.Thread(target=connection_thread, args=(s_peer, peer_addr, peer_port))
peer_private_thread = threading.Thread(target=connection_private_thread, args=(s_peer_private, peer_private_addr, peer_private_port))


peer_thread.start()
peer_private_thread.start()
listen_thread.start()









