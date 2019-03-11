import curses
from copy import copy
class NotEmpty(Exception):
    pass
class IllegalMove(Exception):
    pass
class Ko(Exception):
    pass
        

class Go:
    def neighbourgs(self,x,y):
        #todo
        return []
    def members(self,x,y,color,track=None):
        if track is None:
            track = set()
        #TODO keep track
        return track
    
    def remove(self,x,y):
        m=self.members(x,y,self.d[x,y])
        #TODO real remove
        return m

    def has_liberty(self,x,y,color):
        if self.d.get((x,y),None)==None:
            return False
        for m in self.members(x,y,color):
            for n in self.neighbourgs(x,y):
                if (x,y) not in self.d:
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
    def play(self,x,y,color):
        #print(self.history)
        if (x,y) in self.d:
            raise NotEmpty()
        try:
            self.d[x,y]= color
            removed = []
            for n in self.neighbourgs(x,y):
                if not self.has_liberty(*n,opponent_color(color)):
                    removed.extend(remove(self.d,*n))
            #TODO had this check
            #if not self.has_liberty(x,y,color):
            #    raise IllegalMove()
            #print(len(self.history))
            #print(self.d)
            try:
             #   print(self.history.index(self.d))
                pass
            except:
                pass
            if self.d in self.history:
                try:
                    print(self.history.index(self.d))
                    print(self.history)
                    print(self.d)
                    pass
                except:
                    pass
            
                raise Ko()
        except Exception:
            del self.d[x,y]
            for m in removed:
                self.d[x,y]=opponent_color(color)
            raise
        self.history.append(copy(self.d))
        return (x,y),removed
            
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
    go=Go(5)
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
    (x,y),prisonners=go.play(x-1,y-1,color)
    x,y = x+1,y+1
    win.addch(x,y,color.upper())
    
    a,b=lastmove
    color = "b" if color=="w" else "w"
    if lastmove!=(-1,-1):
        win.addch(a,b,color)
    return (x,y),color
if __name__=="__main__":
    main()
