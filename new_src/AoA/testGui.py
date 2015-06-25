from Tkinter import *
import random

class WNFA_GUI(Frame):
    
    def __init__(self,master=None, coord=[]):
        Frame.__init__(self,master);
        
        self.start_x = -10
        self.start_y = -10
        self.mag = 60   
        self.rows = 9   
        self.cols = 11 
        self.orginal_x = 380
        self.orginal_y = 320  

        canvas_width = 760
        canvas_height = 640
        self.w = Canvas(master, width=canvas_width, height=canvas_height)
        self.w.pack()
        self.drawGrid()
        self.addLabel()
        self.redraw(1000,coord)

    def addLabel(self):
                          
        x_Start = -330
        y_Start = 270
                          
        for i in range(0,self.cols+1):    
            widget_top = Label(self.w, text=x_Start, fg='black')
            widget_buttom = Label(self.w, text=x_Start, fg='black')
            x_Start = x_Start + self.mag
    
            self.w.create_window(50+i*self.mag, 35, window=widget_top) 
            self.w.create_window(50+i*self.mag, 605, window=widget_buttom)

        for i in range(0,self.rows+1):           
            widget_right = Label(self.w, text=y_Start, fg='black')
            widget_left = Label(self.w, text=y_Start, fg='black')
            y_Start = y_Start - self.mag
    
            self.w.create_window(30, 50+i*self.mag, window=widget_right) 
            self.w.create_window(730, 50+i*self.mag, window=widget_left)

    def drawGrid(self):
       
        for i in range(0,self.cols+1):
            self.w.create_line(self.start_x + (i+1)*self.mag, self.start_y + self.mag,\
                               self.start_x + (i+1)*self.mag, self.start_y + (self.rows+1)*self.mag, fill='blue')
        for i in range(0,self.rows+1):
            self.w.create_line(self.start_x + self.mag, self.start_y + (i+1)*self.mag,\
                               self.start_x + self.mag*(1+self.cols), self.start_y + (i+1)*self.mag, fill='blue')
        self.w.create_line(380, 0, 380, 640, fill="#1f1f1f", dash=(4, 4))
        self.w.create_line(0 , 320, 760, 320, fill="#1f1f1f", dash=(4, 4))
        trans1 = self.w.create_oval(375,315,385,325,fill = 'red')
        trans2 = self.w.create_oval(354,336,364,346,fill = 'red')
        trans3 = self.w.create_oval(396,336,406,346,fill = 'red')

    def redraw(self, delay ,coord):
        
        if(len(coord) > 0) :
            # row = random.randint(50,580)
            # col = random.randint(50,700)
            x = self.orginal_x + coord[0][0]
            print "x=",x
            y = self.orginal_y - coord[0][1]
            print "y=",y
    
            trans1 = self.w.create_oval(x,y,x+10,y+10,fill = 'green')

            self.after(delay, lambda: self.redraw(delay, coord))
            del coord[0]

if __name__ == '__main__':
    root = Tk()
    coord = [(2,29),(43,59),(-30,-40),(-60,70),(150,-169)]
    app = WNFA_GUI(master=root, coord=coord)
    app.mainloop()
