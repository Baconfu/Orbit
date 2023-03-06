import tkinter
import math
import time
import random

class Planet:
    def __init__(self,x,y,xv,yv,r):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.xa = 0
        self.ya = 0
        self.m = r * r * math.pi
        self.r = r
        
        
class ThreeBody:
    def __init__(self,root):
        self.root = root
        self.canvas = tkinter.Canvas(self.root,width=600,height = 600,bg = "white")
        self.canvas.place(x=0,y=0)
        self.root.minsize(width=600,height=600)
        self.planets = [Planet(101,100,random.randint(-10,10)/10.0,random.randint(-10,10)/10.0,10),
                        Planet(500,200,random.randint(-10,10)/10.0,random.randint(-10,10)/10.0,12),
                        Planet(250,350,random.randint(-10,10)/10.0,random.randint(-10,10)/10.0,14)]
        
        self.w = 10
        self.h = 10
        self.grid = ["" for i in range(0,(600//self.w)*(600//self.h))]
        
        self.run()
    def check(self,xpos,ypos):
        out = self.grid[int(ypos//self.h*self.w+xpos//self.w)].split(",")
        if len(out)>1:
            out2=[]
            for i in range(1,len(out)):
                out2.append(int(out[i]))
            return out2
        else:
            return []
        
    def register(self,x,y,pid):
        self.grid[int(y//self.h*self.w+x//self.w)] = self.grid[int(y//self.h*self.w+x//self.w)] + ","+str(pid)
        
    def run(self):
        obj = []
        loop=0
        while True:
            for planet in self.planets:
                planet.xa=0
                planet.ya=0
            for i in range(0,len(self.planets)):
                p = self.planets[i]
                plist = self.check(p.x,p.y)
                if len(plist)>0:
                    print(plist)
                self.register(p.x,p.y,i)
            self.grid = ["" for i in range(self.w*self.h)]
                           
            for i in range(0,len(self.planets)-1):
                p1 = self.planets[i]
                for j in range(i+1,len(self.planets)):
                    
                    p2 = self.planets[j]
                    xdist = (p2.x-p1.x)
                    ydist = (p2.y-p1.y)
                    
                    dist = xdist**2 + ydist**2

                    f = 0.005 * p1.m*p2.m / dist
                    if f>0.5:
                        f=0.5

                    angle = math.atan(ydist/xdist)
                    if xdist<0:
                        angle+=math.pi

                    p1.xa += math.cos(angle) * f
                    p1.ya += math.sin(angle) * f

                    p2.xa -= math.cos(angle) * f
                    p2.ya -= math.sin(angle) * f

            for planet in self.planets:
                planet.xv += planet.xa
                planet.yv += planet.ya
                planet.x += planet.xv
                planet.y += planet.yv

            loop+=1
            if loop == 2:
                loop=0
                for planet in self.planets:
                    self.canvas.create_line(planet.x,planet.y,planet.x+1,planet.y)

            for planet in self.planets:
                r = planet.r
                obj.append(self.canvas.create_oval(planet.x-r,planet.y-r,planet.x+r,planet.y+r))
            time.sleep(0.018)
            self.canvas.update()
            for thing in obj:
                self.canvas.delete(thing)
            
            
        
root  = tkinter.Tk()

ThreeBody(root)
root.mainloop()
