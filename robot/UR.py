from ur_programmer import UR_programmer
from rTData import RTData
import tkinter as tk
from math import sin
import time
import socket
import sqlite3
import rest_api as api

prog = UR_programmer("10.130.58.14", simulate=False)
con = sqlite3.connect('data.db')
rtd = RTData()
rtd.connect("10.130.58.14", simulate = False)

inp = ''
print('Kommandoer: ')
print('Socket       - Åbner socket til robot')
print('Hjem         - Flytter sig til hjem position')
print('Path         - Bevæger robot i en path')
print('Get pos      - Få nuværende position i meter')
print('Rød          - Kør til rød')
print('Blå          - Kør til Blå')
print('Lilla        - Kør til lilla')
print('Pink         - Kør til pink')
print('Åben         - Åbner klo')
print('Luk          - Lukker klo')
print('Remove       - Tager en pind og clearer plate')
print('Opret db     - Opretter database')
print('Add          - Tilføj til database')
print('Opret db     - Lav database orders')
print('Tilføj       - Tilføj ordre til database')
print('Status       - Ser status på robot')

#Punkter:
prog.Red_move = b'    movej(p[-0.46767872396762844, -0.3698128835873044, 0.02963185559456491, -2.217932472407618, -2.222047281659294, -0.0015727295386725355])\n'
prog.Blue_move = b'    movej(p[-0.3725509088123165, -0.4680704494476208, 0.029604686116777662, -2.217798272104411, -2.222176627899193, -0.0016518231639489926])\n'
prog.Pink_move = b'    movej(p[-0.3716525461718336, -0.3698075928096446, 0.029599473982834468, -2.2179488026010796, -2.222120088244764, -0.0016251985431207378])\n'
prog.Purple_move = b'    movej(p[-0.46692245864436893, -0.46808077336865894, 0.029610921748734587, -2.2178113553864187, -2.2221030858373014, -0.0016967473819248587])\n'
prog.Kop_move = b'    movej(p[-0.4065437681072872, -0.002418697295223622, 0.1690680827318533, -2.217976025883232, -2.222246788559907, -0.0015539678724949641])\n'
prog.Hover_move = b'    movej(p[-0.4121797433628598, -0.4184062836040695, 0.08139044773530577, -2.2179206669309033, -2.222198154631676, -0.001408599175344454])\n'
prog.Stick_move = b'    movej(p[-0.47775575448931235, -0.1988892490740506, 0.021096244513058332, -2.217857467590136, -2.2222498562643205, -0.001498164332685943])\n'

while not inp.startswith('q'):
    inp = input('> ')
    
    if inp == 'Socket':
        prog.s.send(b'def myProg():\n')
        prog.s.send(b'  popup("test")\n')
        #prog.s.send(b'  open=socket_open("10.130.58.35",21)\n')
        #prog.s.send(b'  while open==False:\n')
        #prog.s.send(b'    open=socket_open("10.130.58.35",21)\n')
        #prog.s.send(b'  targetPos=p[0,0,0,0,0,0]\n')
        #prog.s.send(b'  counter=0')
        #prog.s.send(b'  sendToServer="send to server"')
        #prog.s.send(b'  socket_send_string(sendToServer)')
        #prog.s.send(b'  receiveFromServ=socket_read_ascii_float(6)')
        #prog.s.send(b'Loop receiveFromServ[0]!=6')
        #prog.s.send(b'     Wait: 0.3')
        #prog.s.send(b'     receiveFromServ≔socket_read_ascii_float(6)')
        #prog.s.send(b'     Loop counter<6')
        #prog.s.send(b'targetPos[counter]=receiveFromServ[counter+1]')
        #prog.s.send(b'counter≔counter+1')
        #prog.s.send(b'MoveJ targetPos')
        #prog.s.send(b'counter:=0')      
        prog.s.send(b'end\n')
        print('Socket åben')
    
    elif inp == "Hjem":
        #Hjem er defineret i ur_programmer - linje 18
        #Prædefineret home-position:
        #(Når vi skal sende en streng til robotten,
        # skal den konverteres til et bytearray
        # derfor står der b foran strengen.)
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.home_pos)
        prog.s.send(b'end\n')
    
    elif inp == "Path":
        prog.move_path([[-0.404,-0.416],[-0.304,-0.416],[-0.304,-0.316]])

    elif inp == "Get pos":
        print(rtd.tool_frame)
    
    elif inp == "Rød":
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.Red_move)
        prog.s.send(b'end\n')

    elif inp == "Blå":
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.Blue_move)
        prog.s.send(b'end\n')

    elif inp == "Lilla":
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.Purple_move)
        prog.s.send(b'end\n')

    elif inp == "Pink":
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.Pink_move)
        prog.s.send(b'end\n')

    elif inp =='Kop':
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.Kop_move)
        prog.s.send(b'end\n')

    elif inp =='Hover':
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.Hover_move)
        prog.s.send(b'end\n')

    elif inp =='Stick':
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.Stick_move)
        prog.s.send(b'end\n')

    elif inp =="Remove":
        TCP_PORT = 29999
        BUFFER_SIZE = 1024
        TCP_IP = "10.130.58.14"#INDTAST DEN RIGTIGE IP-ADRESSE HER!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect((TCP_IP, TCP_PORT))
            response = s.recv(BUFFER_SIZE)
        except socket.error:
            print("Socket error")
            s.close()

        st = "load /programs/henrik3d/remove.urp\n"
        s.send(bytearray(st,'utf8'))
        response = s.recv(BUFFER_SIZE)
        s.send(b"play\n")
        response = s.recv(BUFFER_SIZE)
        s.close()

    elif inp =="Luk":
        TCP_PORT = 29999
        BUFFER_SIZE = 1024
        TCP_IP = "10.130.58.14"#INDTAST DEN RIGTIGE IP-ADRESSE HER!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect((TCP_IP, TCP_PORT))
            response = s.recv(BUFFER_SIZE)
        except socket.error:
            print("Socket error")
            s.close()

        st = "load /programs/henrik3d/luk.urp\n"
        s.send(bytearray(st,'utf8'))
        response = s.recv(BUFFER_SIZE)
        s.send(b"play\n")
        response = s.recv(BUFFER_SIZE)
        s.close()

    elif inp =="Åben":
        TCP_PORT = 29999
        BUFFER_SIZE = 1024
        TCP_IP = "10.130.58.14"#INDTAST DEN RIGTIGE IP-ADRESSE HER!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect((TCP_IP, TCP_PORT))
            response = s.recv(BUFFER_SIZE)
        except socket.error:
            print("Socket error")
            s.close()

        st = "load /programs/henrik3d/open.urp\n"
        s.send(bytearray(st,'utf8'))
        response = s.recv(BUFFER_SIZE)
        s.send(b"play\n")
        response = s.recv(BUFFER_SIZE)
        s.close()

    elif inp == "Opret db":
        try:
            con.execute("""CREATE TABLE orders (
                orderID STRING,
                ting1 INTEGER,
                ting2 INTEGER, 
                ting3 INTEGER)""")
            print('Tabel 1 oprettet')
            con.commit()
        except Exception as e:
            print('Tabellen findes allerede/fejl opstod')
    
    elif inp == "Tilføj":
        orderID = input('Indtast orderID: ')
        ting1 = input('Indtast farve 1: ')
        ting2 = input('Indtast farve 2: ')
        ting3 = input('Indtast farve 3: ')
        c = con.cursor()
        c.execute('INSERT INTO orders (orderID,ting1,ting2,ting3) VALUES (?,?,?,?)', (orderID,ting1,ting2,ting3))
        con.commit()

    elif inp == "Vis":
        c = con.cursor()
        c.execute('SELECT orderID,ting1,ting2, ting3 FROM orders')

    elif inp == "Status":
        api.robot_order_get()
    
        