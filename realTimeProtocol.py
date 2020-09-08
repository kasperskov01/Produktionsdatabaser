from rTData import RTData
import tkinter as tk
import socket
from math import sin
import time

class RealTimeProtocol(tk.Frame):
    def __init__(self, master=None):

        self.millis = int(round(time.time() * 1000))

        tk.Frame.__init__(self, master)
        self.grid()

        self.robot = RTData()
        self.build_GUI()

        self.robot.connect("10.130.58.14", False)

        self.after(100, self.update)
        self.t = 0

        self.cycle_active = False
        self.run_timed_command()


        #Socket til at sende kommandoer til robotten
        TCP_IP = "10.130.58.14"
        TCP_PORT = 30002
        BUFFER_SIZE = 1024

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)
        try:
            #print("Opening IP Address" + TCP_IP)
            self.s.connect((TCP_IP, TCP_PORT))
            response = self.s.recv(BUFFER_SIZE)
        except socket.error:
            print("Socket error")
            self.s.close()



    def update(self):
        self.set_robot_pos()
        #Call again in 100 ms
        self.after(100, self.update)

    #Virker ikke?
    #Robotten disconnecter og tk stopper mainloop,
    #men vinduet fortsætter?
    def exit_program(self):
        self.s.close()
        self.robot.disconnect()
        self.destroy()

    def send_home_command(self):
        #PI/2 : 1,5708
        #s.send(b'def myProg():\n')
        #s.send(b'  var_1=[0,-1.5708, 1.5708, -1.5708, -1.5708, 0]\n')#fri
        self.s.send(b'  movej([0,-1.5708, 1.5708, -1.5708, -1.5708, 0])\n')
        #s.send(b'end\n')


    def run_timed_command(self):
        if self.cycle_active == True:
            self.millis = int(round(time.time() * 1000))
            for i in range(0,1):
                self.t = self.t + 0.008
                #Default: , lookahead_time = 0.1, gain=300

                #Joint mode,
                #j0 = sin(self.t*0.3)*30*2*3.1415/360
                #st = 'servoj([{},-1.5708, 1.5708, -1.5708, -1.5708, {}], t=0.2)\n'.format(j0, j0)

                #Cartesian mode
                '''x0 = -0.487 + sin(self.t*0.2)*0.1
                y0 = -0.108 + sin(1+self.t*0.25)*0.1
                z0 = 0.245# + sin(self.t*0.3)*0.01
                ax0 = 3.14
                ay0 = 0
                az0 = 0
                self.s.send(b'def myProg():\n')
                st = '    xpose = get_inverse_kin(p[{},{},{}, {}, {}, {}])\n'.format(x0, y0, z0, ax0, ay0, az0)
                self.s.send(bytearray(st,'utf8'))
                st = '    servoj(xpose, t=0.01, gain=100)\n'.format(x0, y0, z0, ax0, ay0, az0)
                self.s.send(bytearray(st,'utf8'))
                if int(self.t) %4 == 0:
                    print(x0,y0,z0,ax0,ay0,az0)
                self.s.send(b'end\n')
                '''

                #speed mode
                j0 = sin(self.t*0.2)*45*2*3.1415/360
                jac = self.robot.qactual[0]
                diff = j0-jac
                sp = 0.1*diff
                #print(j0, sp)
                st = 'speedj([{},0, 0, 0, 0, 0], a=0.5)\n'.format(sp)
                self.s.send(bytearray(st,'utf8'))

        self.after(8, self.run_timed_command)

    def activate_cycle(self):
        self.cycle_active = not self.cycle_active
        self.t = 0


    def set_robot_pos(self):
        self.scale0.set(self.robot.qactual[0]*360/(2*3.1415))
        self.scale1.set(self.robot.qactual[1]*360/(2*3.1415))
        self.scale2.set(self.robot.qactual[2]*360/(2*3.1415))
        self.scale3.set(self.robot.qactual[3]*360/(2*3.1415))
        self.scale4.set(self.robot.qactual[4]*360/(2*3.1415))
        self.scale5.set(self.robot.qactual[5]*360/(2*3.1415))
        self.program_state.configure(text='Program state: ' + str(self.robot.program_state))

    def build_GUI(self):
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side = tk.BOTTOM)

        topFrame = tk.Frame(self)
        topFrame.pack(side = tk.TOP)

        leftFrame = tk.Frame(topFrame)
        leftFrame.pack(side = tk.LEFT)

        rightFrame = tk.Frame(topFrame)
        rightFrame.pack(side = tk.RIGHT)

        #butDisconnect = tk.Button(rightFrame, text='Afbryd forbindelse', command=self.exit_program)
        #butDisconnect.pack(fill = tk.X)

        self.scale0 = tk.Scale(bottomFrame, label='Base', from_=-360, to=360, length=200, orient=tk.HORIZONTAL)
        self.scale0.pack(fill=tk.X)
        self.scale1 = tk.Scale(bottomFrame, label='Shoulder', from_=-360, to=360, length=200, orient=tk.HORIZONTAL)
        self.scale1.pack(fill=tk.X)
        self.scale2 = tk.Scale(bottomFrame, label='Elbow', from_=-360, to=360, length=200, orient=tk.HORIZONTAL)
        self.scale2.pack(fill=tk.X)
        self.scale3 = tk.Scale(bottomFrame, label='Wrist 1', from_=-360, to=360, length=200, orient=tk.HORIZONTAL)
        self.scale3.pack(fill=tk.X)
        self.scale4 = tk.Scale(bottomFrame, label='Wrist 2', from_=-360, to=360, length=200, orient=tk.HORIZONTAL)
        self.scale4.pack(fill=tk.X)
        self.scale5 = tk.Scale(bottomFrame, label='Wrist 3', from_=-360, to=360, length=200, orient=tk.HORIZONTAL)
        self.scale5.pack(fill=tk.X)

        butSendHome = tk.Button(rightFrame, text='Home', command=self.send_home_command)
        butSendHome.pack(fill=tk.X)
        butStartCycle = tk.Button(rightFrame, text='Start cycle', command=self.activate_cycle)
        butStartCycle.pack(fill=tk.X)

        self.program_state = tk.Label(bottomFrame, text='Program state: ')
        self.program_state.pack(fill=tk.X)



prg = RealTimeProtocol()

prg.master.title('Realtime Robot Control')

prg.mainloop()
