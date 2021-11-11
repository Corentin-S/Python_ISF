"""
READ ME:
    Ce code contient trois parties. Une première modélisant le jeu de la vie
de Conway en lui même. La seconde partie concerne la première fenêtre graphique.
La dernière partie du code permet de construire l'interface graphique principale.

L'interface a été conçu pour être simple à appréhender pour l'utilisateur.
Dans un premier temps, on choisit la taille de l'interface. Il est ensuite possible
de régler plusieurs paramètres comme la vitesse, la couleur ou la taille des
carreaux. Utiliser le bouton 'apply' pour valider vos choix puis sur 'start'
pour commencer le jeu. Il est possible de mettre sur pause avec le bouton
'stop' ou de changer la vitesse pendant la partie.

Vous pouvez recommencer le jeu à l'infini en modifiant les paramètres puis en
appuyant sur 'apply' et de nouveau sur 'start'.
NB: Il n'est pas conseillé de changer manuellement la taille de l'écran.
"""


import numpy as np
import numpy.random as sim
import tkinter as tk
import copy
import time


square_size = 20
square_color = 'black'
background_color = 'white'
alea = 5
final_time = 100000
speed = 1
start = True


window0_height = 100
window0_width = 350
button_height = 2
button_width = 6
options_window_width = 200
options_window_height = 400


font_helv18 = ('Helvetica', '18', 'bold')
font_helv12 = ('Helvetica', '12')
 


'''-------------------------------------------------------------------------------------------'''



'''Conway's game of Life'''
'''-------------------------------------------------------------------------------------------'''


def grid_construction():
    
    
    stop()
    canvas.delete("all")
    canvas.create_polygon(0 ,0 ,options_window_width ,0 ,\
      options_window_width ,options_window_height, 0, options_window_height, fill = 'lightgrey')
   
         
    canvas.create_polygon(options_window_width ,options_window_height, 0, options_window_height,\
                      0 , height, options_window_width, height, fill = 'dimgray')
           
        
        
    canvas.create_line(options_window_width-1 ,0 ,options_window_width-1, height, \
                   fill = 'black', width = 2)
          
         
    global line_size
    global col_size
    global identifier
    global grid0
    
    line_size = int(width / square_size)
    col_size = int(height / square_size)
    identifier = np.zeros((line_size,col_size))
    grid0 = np.zeros((line_size+2,col_size+2))
        
    
    
    
    
    for i in range(1,line_size+1):
        for j in range(1,col_size+1):
            grid0[i,j] = int(sim.randint(0, alea + 1) / alea)
            identifier[i-1,j-1] = canvas.create_polygon(
                options_window_width + square_size * (i-1), square_size * (j-1), 
                options_window_width + square_size * (i-1), square_size * j, 
                options_window_width + square_size * i, square_size * j, 
                options_window_width + square_size * i, square_size * (j-1),
                fill = square_color, state = 'hidden')
    





def refresh_canvas(grid):
    for i in range(1,line_size+1):
        for j in range(1,col_size+1):
            if (grid[i,j] == 1):
                canvas.itemconfigure(int(identifier[i-1,j-1]), state = 'normal')
            else:
                canvas.itemconfigure(int(identifier[i-1,j-1]), state = 'hidden')
    canvas.update()





def neighbours(i,j,grid):
    return (grid[i-1,j-1] + grid[i-1,j] + grid[i-1,j+1] +
            grid[i,j-1]   +               grid[i, j+1]  +
            grid[i+1,j-1] + grid[i+1,j] + grid[i+1,j+1] ) 




def refresh_grid(grid):
    
    old_grid = np.zeros((line_size+2,col_size+2))
    old_grid = copy.deepcopy(grid)

    for i in range(1,line_size+1):
        for j in range(1,col_size+1):  
            nbr_neighs = neighbours(i,j,old_grid)
            grid[i,j] = (nbr_neighs == 3) * (old_grid[i,j] == 0) + \
                (old_grid[i,j] == 1) * (nbr_neighs == 2 or nbr_neighs == 3)
                
    return grid




def canvas_loop(grid):
    
    global start
    start = True
    
    for s in range(final_time):
        
        refresh_canvas(grid)
        time.sleep(0.1/speed)
        grid = refresh_grid(grid)
        
        if (start == False):
            return grid
        
    return grid





'''-------------------------------------------------------------------------------------------'''



'''First Window'''
'''-------------------------------------------------------------------------------------------'''


window0 = tk.Tk()
window0.geometry(str(window0_width) + 'x' + str(window0_height))
window0.title('Conway\'s Game of Life')


def set_window_size(size):
    global width
    global height
    width = size
    height = size
    window0.destroy()



def create_first_window():
    
    label = tk.Label(window0, text = 'Choose the size of the grid !', font = font_helv18)


    tiny_button = tk.Button(window0, text="Tiny", activebackground = 'grey', \
                          command=lambda *args: set_window_size(400), anchor = tk.CENTER,
                          height = button_height, width = button_width, font = font_helv12,
                          cursor = 'hand2')

    medium_button = tk.Button(window0, text="Medium", activebackground = 'grey', \
                       command = lambda *args: set_window_size(600),anchor = tk.CENTER,
                       height = button_height, width = button_width, font = font_helv12,
                       cursor = 'hand2')
    
    big_button = tk.Button(window0, text="Big", activebackground = 'grey', \
                       command = lambda *args: set_window_size(700),anchor = tk.CENTER,
                       height = button_height, width = button_width, font = font_helv12,
                       cursor = 'hand2')
    
    giant_button = tk.Button(window0, text="Giant", activebackground = 'grey', \
                          command=lambda *args: set_window_size(800),anchor = tk.CENTER,
                          height = button_height, width = button_width, font = font_helv12,
                          cursor = 'hand2')

    
    label.place(x = 5 , y = (window0_width / 100))

    x0 = window0_width / 100 ; y0 = window0_height / 2.5

    tiny_button.place(x = x0, y = y0)
    medium_button.place(x = x0 * 26, y = y0)
    big_button.place(x = x0 * 51, y = y0)
    giant_button.place(x = x0 * 76, y = y0)
    


create_first_window()
window0.mainloop()





'''-------------------------------------------------------------------------------------------'''


'''Main Window'''
'''-------------------------------------------------------------------------------------------'''


window = tk.Tk()
window.title('Conway\'s Game of Life')

canvas = tk.Canvas(window, width= options_window_width + width, \
                   height=height, background = background_color)
canvas.pack()



    
def change_speed(value):
    global speed
    speed = float(value)
    



def stop():
    global start
    start = False
    
    

   
def create_options_window():
    
    
    
    speed_scale = tk.Scale(window, orient='horizontal', from_=1, to=5, \
      resolution=1, length=options_window_width - 10, sliderrelief = 'flat',\
      command = change_speed, font = font_helv18, troughcolor ='grey', 
      label = '       Speed', bg ='lightgrey',cursor = 'hand2')





    start_button = tk.Button(window, text="START", activebackground = 'grey', 
                          anchor = tk.CENTER, command = lambda *args: canvas_loop(grid0),
                          height = button_height, width = button_width, font = font_helv12,
                          cursor = 'hand2')
        
    
    
    stop_button = tk.Button(window, text="STOP", activebackground = 'grey', \
                          command = lambda *args: stop(), anchor = tk.CENTER,
                          height = button_height, width = button_width, font = font_helv12,
                          cursor = 'hand2')
    
        
        
     
        
        
    def change_square_color():
        global square_color
        square_color = var1.get()        
        
   
    
    tk.Label(window, text = 'Square color', font = font_helv18, \
             bg = 'lightgrey').place(x = 20, y = 25 * options_window_height / 100)
                                                    
    
    labels = ['Black', 'Green', 'Blue', 'Orange', 'Purple', 'Red']
    values = ['black', 'green', 'darkturquoise', 'orange', 'purple', 'salmon']
    var1 = tk.StringVar()
    
    
    for i in range(3):
        tk.Radiobutton(window,text = labels[i], value = values[i], variable = var1, \
                       command = change_square_color, bg = 'lightgrey' \
                       ).place(x = 70 * i ,y = 35 * options_window_height / 100)
            
    for i in range(3):
        tk.Radiobutton(window,text = labels[i+3], value = values[i+3], variable = var1, \
                       command = change_square_color, bg = 'lightgrey' \
                       ).place(x = 70 * i ,y = 40 * options_window_height / 100)
    
    
    
    
    
    
    
    
    def change_square_size():
        global square_size
        square_size = var2.get()        
        
        
    tk.Label(window, text = 'Square size', font = font_helv18, \
             bg = 'lightgrey').place(x = 25, y = 50 * options_window_height / 100)
                                                    
    
    labels = ['Small', 'Medium', 'Big']
    values = [10, 20 , 25]
    var2 = tk.IntVar()
    for i in range(len(values)):
        tk.Radiobutton(window,text = labels[i], value = values[i], variable = var2, \
                       command = change_square_size, bg = 'lightgrey' \
                       ).place(x = 70 * i ,y = 60 * options_window_height / 100)
    
    
    
    
    

                                                 
                                                           
    restart_button = tk.Button(window, text="APPLY", activebackground = 'grey', \
                          command = lambda *args: grid_construction(), anchor = tk.CENTER,
                          height = button_height, width = button_width, \
                         font = font_helv12, cursor = 'hand2')
    
    
        
        
        
    speed_scale.place(x = 0 ,y = options_window_height / 100)
    restart_button.place(x = 60 ,y = 70 * options_window_height / 100, width = 2/5 * options_window_width)
    start_button.place(x = 10 ,y = options_window_height - 60, width = 2/5 * options_window_width)
    stop_button.place(x = options_window_width / 2 + 10 ,y = options_window_height - 60,\
                      width = 2/5 * options_window_width)




grid_construction()
create_options_window()
window.mainloop()


'''-------------------------------------------------------------------------------------------'''




