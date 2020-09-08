from ur_programmer import UR_programmer
from rTData import RTData
import tkinter as tk
from math import sin
import time
import socket

prog = UR_programmer("10.130.58.14", simulate=False)

inp = ''
rtd = RTData()
rtd.connect("10.130.58.14", simulate = False)
print('')
print('Kommandoer: ')
print('Socket       - Åbner socket på robot')
print('Hjem         - Flytter sig til hjem position')
print('Path         - Bevæger robot i en path')
print('Get pos      - Få nuværende position i meter')
print('Rød          - Kør til rød')
print('Blå          - Kør til Blå')
print('Lilla        - Kør til lilla')
print('Pink         - Kør til pink')

#Punkter:
prog.Red_move = b'    movej(p[-0.46694534589480835, -0.37128454680967377, 0.04719900890326209, -2.2179237839798986, -2.22213649039662, -0.0015964512197490473])\n'
prog.Blue_move = b'    movej(p[-0.3693862960510677, -0.46808488913304924, 0.04724995447689745, -2.2179385532480334, -2.2220897902105032, -0.0014254072396997683])\n'
prog.Pink_move = b'    movej(p[-0.3693534253982512, -0.37132993152269583, 0.047187788409537745, -2.2179978175123582, -2.222064216064882, -0.0016359576113810165])\n'
prog.Purple_move = b'    movej(p[-0.46692173996805797, -0.468102314883946, 0.047183831068495635, -2.2179022788830376, -2.2221380390946655, -0.0016503394839434411])\n'

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