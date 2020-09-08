from ur_programmer import UR_programmer

prog = UR_programmer("10.130.58.14", simulate=False)

inp = ''

print('')
print('Kommandoer: ')
print('Socket       - Åbner socket på robot')
print('Hjem         - Flytter sig til hjem position')
print('Path         - Bevæger robot i en path')
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
        #Prædefineret home-position:
        #(Når vi skal sende en streng til robotten,
        # skal den konverteres til et bytearray
        # derfor står der b foran strengen.)
        prog.s.send(b'def myProg():\n')
        prog.s.send(prog.home_pos)
        prog.s.send(b'end\n')

    elif inp == "Path":
        prog.move_path([[-0.404,-0.416],[-0.304,-0.416],[-0.304,-0.316]])