import curses
from copy import copy
class NotEmpty(Exception):
    pass
class IllegalMove(Exception):
    pass

def members(x,y,color,track=None):
    if track is None:
        track = set()
    #TODO
def hasliberty(x,y,color):
    if self.d.get((x,y),None)==None:
        return False
    for m in members(x,y,color):
        for n in neighbourgs(x,y):
            if x,y not in d:
                return True
class Go:
    def __init__(self,size):
        self.size=size
        self.d = {}
        for i in range(size):
            self.d[-1,i] = "/"
            self.d[i,-1] = "/"
            self.d[size,i] = "/"
            self.d[i,size] = "/"
        self.history=[copy(self.d)]    
    def play(self,x,y,color):
        
        if not x,y in d:
            raise NotEmpty()
        try:
            self.d[x,y]= color
            removed = []
            for n in neighbourgs(x,y):
                if not hasliberty(*n,opponent_color(color)):
                    removed.extend(remove(*n))
            if not hasliberty(x,y,color):
                raise IllegalMove()
            if self.d in self.history:
                raise Ko()
        except Exception:
            del self.d[x,y]
            raise
            
def main():
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
    go=Go()
    x,y=0,0
    lastmove=-1,-1
    win.refresh()
    color="b"

    while True:
        win.move(x,y)
        win.refresh()
        k=win.getch()
        #print(curses.KEY_ENTER)
        if curses.KEY_LEFT==k: y-=1
        elif curses.KEY_RIGHT==k: y+=1
        elif curses.KEY_UP==k: x-=1
        elif curses.KEY_DOWN==k: x+=1

        elif curses.KEY_ENTER==k or k==10 or k==13:lastmove,color=play(go,win,color,lastmove,x,y)
        elif curses.KEY_MOUSE:
            (id, y, x, z, bstate)=curses.getmouse()
            lastmove,color=play(win,color,lastmove,x,y)
        else:print("bad key",k)
        mx,my= win.getmaxyx()
        x%=7
        y%=7
    

        
def play(go,win,color,lastmove,x,y):
#    return
    #print(lastmove)
    if not(1<=x<=5 and 1<=y<=5):
        return lastmove,color
    (x,y),prisonners=go.play(x,y,color)
    win.addch(x,y,color.upper())
    
    a,b=lastmove
    color = "b" if color=="w" else "w"
    if lastmove!=(-1,-1):
        win.addch(a,b,color)
    return (x,y),color
if __name__=="__main__":
    main()
