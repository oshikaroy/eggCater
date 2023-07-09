from itertools import cycle
from random import randrange
from tkinter import Image, Tk , Canvas , messagebox , font
from PIL import Image,ImageTk

canvas_width = 900
canvas_height = 500
win = Tk()
#background image
c = Canvas(win , width = canvas_width , height = canvas_height )
img=Image.open(r"D:\SEM VI\Computer Graphics\360_F_108322631_sY7YxNYI0xSpRmoeZoPyUfZTg7AtYwJG.jpg")
c.image=ImageTk.PhotoImage(img)
c.create_image(0,0,image=c.image,anchor='nw')

c.pack()

#EGG
color_cycle = cycle(['blue' ,'violet', 'pink' , 'yellow','green' ,
'red','black'])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty_factor = 0.95

#EGG CATCHER
catcher_color = 'black'
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height -catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height
catcher = c.create_arc(catcher_start_x ,catcher_start_y
                       ,catcher_start_x2,catcher_start_y2 , start=200 , extent = 140 , style='arc' ,
                        outline=catcher_color , width=6)

#SCORE
score = 0
score_text = c.create_text(10,10,anchor='nw' ,
font=('Arial',18,'bold'),fill='white',text='Score : ' + str(score))

#LIVES REMAINING
lives_remaning = 3
lives_text = c.create_text(canvas_width-10,10,anchor='ne' ,
font=('Arial',18,'bold'),fill='white',text='Lives : ' + str(lives_remaning))
eggs = []

#EGG CREATION
def create_eggs():
    x = randrange(10,740)
    y = 40
    new_egg =c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs)

#MOTION OF EGG
def move_eggs():
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        c.move(egg,0,15)
        if egg_y2 > canvas_height:
            egg_dropped(egg)
    win.after(egg_speed,move_eggs)

# IF EGG IS MISSED
def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaning == 0:
        messagebox.showinfo('GAME OVER!' , 'Final Score : ' + str(score))
    win.destroy()

#LOSING LIFE
def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    c.itemconfigure(lives_text , text='Lives : ' + str(lives_remaning))

# EGG CATCH CHECKER
def catch_check():
    (catcher_x,catcher_y,catcher_x2,catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2<40:
            eggs.remove(egg)
        c.delete(egg)
        increase_score(egg_score)
    win.after(100,catch_check)

# SCORE INCREASING
def increase_score(points):
    global score , egg_speed , egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text , text='Score : ' + str(score))

# MOVEMENT OF EGG-CATCHER FROM RIGHT TO LEFT
def move_left(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher,-40,0)

def move_right(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher,40,0)

c.bind('<Left>' , move_left)
c.bind('<Right>' , move_right)
c.focus_set()
win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)
win.mainloop()