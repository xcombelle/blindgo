PORT = 8991
import json
import sys
import socket
import threading
import curses
import traceback
from copy import copy
class IllegalMove(Exception):
    pass
class NoLiberty(IllegalMove):
    pass
class NotEmpty(IllegalMove):
    pass
class Ko(IllegalMove):
    pass
class NotYourTurn(IllegalMove):
    pass

class Go:

    def neighbourgs(self,x,y):
        #todo
        for dx,dy in (-1,0),(1,0),(0,-1),(0,1):
            yield (x+dx,y+dy)

    def members(self,x,y,color,track=None):
        if track is None:
            track = set()
        
        if (x,y) in track:
            return track
        if self.d.get((x,y),None)!=color:
            return track

        track.add((x,y))
        for n in self.neighbourgs(x,y):
            self.members(*n,color,track)
        return track
    
    def remove(self,x,y):

        m=self.members(x,y,self.d[x,y])
        for intersection in m:
            print("deleting",intersection,file=open("debug.txt","a"))
            del self.d[intersection]
        
        return m

    def has_liberty(self,x,y,color):

        if self.d.get((x,y),None)!=color:
            return True
        for m in self.members(x,y,color):
            for n in self.neighbourgs(*m):
                if n not in self.d:
                    return True

        return False
    def __init__(self,size):
        self.size=size
        self.d = {}
        for i in range(size):
            self.d[-1,i] = "/"
            self.d[i,-1] = "/"
            self.d[size,i] = "/"
            self.d[i,size] = "/"
        self.history=[copy(self.d)]
        self.current_color="b"


    def play(self,color,x,y):
        
        if color != self.current_color:
            
            raise NotYourTurn("{} != {}".format(color,self.current_color))
        if (x,y) in self.d:
            raise NotEmpty()
        try:
            self.d[x,y]= color
            removed = []
            for n in self.neighbourgs(x,y):
                if not self.has_liberty(*n,opponent_color(color)):
                    print("captured",*n,file=open("debug.txt","a"))
                    removed.extend(self.remove(*n))
            
            if not self.has_liberty(x,y,color):
                raise NoLiberty()
            
            if self.d in self.history:            
                raise Ko()
        except IllegalMove:
            del self.d[x,y]
            for m in removed:
                
                self.d[m]=opponent_color(color)
            raise
        self.history.append(copy(self.d))
        self.current_color="b" if self.current_color=="w" else "w"
        for b in range(-1,7):
            for a in range(-1,7):
                print(self.d.get((a,b)," "),file=open("debug.txt","a"),end="")
            print(file=open("debug.txt","a"))

        return (x,y),removed
def client_file(go,win,f,my_color):
    global lastmove, color

    for l in f:
        print(my_color,"receving move",l,file=open("debug.txt","a"))
    
        position=json.loads(l)
        if position == "error":
            sys.exit(0)
        position[0]+=1
        position[1]+=1
        lastmove,color,r=play(f,{"b":"black","w":"white"}[go.current_color],go,win,color,lastmove,*position)
        print(my_color,"new color",color,file=open("debug.txt","a"))
        win.refresh()
def client(my_color,addr):
    global lastmove, color
    #addr = socket.getaddrinfo(addr, 9999)
    #af, socktype, proto, canonname, sa = res
    s = socket.socket()
    s.connect((addr,PORT))
    f = s.makefile("rw")
    to_send=json.dumps(my_color)
    print("sending",to_send)
    print(to_send,file=f)
    f.flush()
    go=Go(5)
    l = f.readline()
    print("history",l)
    history=json.loads(l)

    x,y=0,0
    lastmove=-1,-1
    color="b"

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.nonl()
    curses.mousemask(curses.BUTTON1_CLICKED)
    win= curses.newwin(8,8,0,0)
    win.keypad(True)

    win.addstr(0,0,"""|||||||
|     |
|     |
|  '  |
|     |
|     |
|||||||"""
    )

    win.refresh()

            
    for p in history:
        p[0]+=1
        p[1]+=1
        lastmove,color,r=play(f,{"b":"black","w":"white"}[go.current_color],go,win,color,lastmove,*p)

        win.refresh()
        color = go.current_color

    threading.Thread(target=client_file, args=(go,win,f,my_color)).start()
    


    while True:
        win.move(x,y)
        win.refresh()
        k=win.getch()

        if curses.KEY_LEFT==k: y-=1
        elif curses.KEY_RIGHT==k: y+=1
        elif curses.KEY_UP==k: x-=1
        elif curses.KEY_DOWN==k: x+=1

        elif curses.KEY_ENTER==k or k==10 or k==13:
            lastmove,color,r=play(f,my_color,go,win,color,lastmove,x,y)
            if r:
                print(json.dumps([x-1,y-1]),file=f)
            f.flush()
        elif curses.KEY_MOUSE:
            o=x,y
            (id, y, x, z, bstate)=curses.getmouse()
            
            lastmove,color,r=play(f,my_color,go,win,color,lastmove,x,y)
            if r:
                print(json.dumps([x-1,y-1]),file=f)
            f.flush()
            if not r:
                x,y=o
        else:print("bad key",k)
        mx,my= win.getmaxyx()
        x%=7
        y%=7
    
def opponent_color(color):
    return "b" if color=="w" else "w"
        
def play(f,turn_color,go,win,color,lastmove,x,y):

    if {"black":"b","white":"w"}[turn_color] !=color:
        print("not your turn",x,y,file=open("debug.txt","a"))
        return lastmove,color,False

    
    if not(1<=x<=5 and 1<=y<=5):
        print("not in range",x,y,file=open("debug.txt","a"))
        return lastmove,color,False

    ox,oy =x,y
    (x,y),prisonners=go.play(color,ox-1,oy-1)
    print("succeed",ox,oy,file=open("debug.txt","a"))
    f.flush()
    x,y = x+1,y+1
    win.addch(x,y,color.upper())
    
    a,b=lastmove
    color=opponent_color(color)
    if lastmove!=(-1,-1):
        win.addch(a,b,color)
    for a,b in prisonners:
        win.addch(a+1,b+1," ")
    print("returning",ox,oy,file=open("debug.txt","a"))
    return (x,y),color,True


d_clients = {}


history = []
    
def server_one(f):
    print(f)
    color = None
    try:
        l=f.readline()
        print("color",l)
        
        color = json.loads(l)
        if color == "white" or color == "black":
            d_clients[color] = f
            print("sending",history)
            print(json.dumps(history),file=f)
            f.flush()
        
            for l in f:
                print("move",l)
                position = json.loads(l)
                go.play("b" if color=="black" else "w",*position)
                history.append(position)
                
                opp = d_clients.get("white" if color=="black" else "black",None)
                if opp is not None:
                    print("sending position to opponent",opp,position)
                    print(json.dumps(position),file=opp)
                    opp.flush()
        else:
            return 
    except :
        traceback.print_exc()
        if color in d_clients:
            del d_clients[color]
            print(json.dumps("error"),file=f)
        f.close()
        

def server():
    global go
    #res = socket.getaddrinfo(addr, 9999)
    #print(res)
    #af, socktype, proto, canonname, sa = res

    s = socket.socket()

    
    s.bind(("0.0.0.0",PORT))
    s.listen(1)
    go=Go(5)
    conns = []
    try:
        while True:
            conn,addr = s.accept()
            with conn:
                print('Connected by', addr)
                conns.append(conn)
                threading.Thread(target=server_one,args=(conn.makefile("rw"),)).start()
    except:
        traceback.print_exc()
        s.close()
        for conn in conns:
            try:
                conn.close()
            except:
                traceback.print_exc()
                
if __name__=="__main__":

    if sys.argv[1] == "server":
        server()
    else:
        try:
            client(sys.argv[1],sys.argv[2])
        except:
            curses.endwin()
            curses.mousemask(0)
            raise
