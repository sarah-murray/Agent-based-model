"""
Create agents in space. Move agents and interact with environment.

Import .csv environmental data and create agents at locations imported 
from web data or, if no data available, at random locations. Move agents
by one step at a time. Where the value of the environmental data exceeds
10, take 10 from the environment and add 10 to the agent store. When
agents are within range of each other, share the data in store equally.

Args:
    num_of_agents (int) -- number of agents.
    num_of_iterations (int) -- number of times agents move.
    neighbourhood (int, float) -- minimum distance between agents before
        they share data.
    total_fill (int, float) -- maximum data storage of each agent.
    carry_on (bool) -- when true, programme continues

Returns:
    dataout.csv -- The edited environmental data.
    data_eaten.csv -- Total data storage of agents.
"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.backends.backend_tkagg
import tkinter #GUI
import agentframework #import the agent module
import matplotlib.pyplot #plot data in graphs
import matplotlib.animation #animate
import random #generate random numbers
import datetime #time the code
import csv #library for handling csv files
import requests #access data url
import bs4 #webscraping

#variables
num_of_agents = 10 #control number of agents created
num_of_iterations = 10 #control the number of iterations
neighbourhood = 20 #control how close agents have to be to share resources
total_fill = 1000 #maximum data store


def getTimeMS():
    """
    Record current time.
    
    Returns:
    Time registered by machine.
    """
    dt = datetime.datetime.now()
    return dt.microsecond + (dt.second*1000000)+\
    (dt.minute*1000000*60) + (dt.hour*1000000*60*60)
  
start = getTimeMS() #start timer

#import html table and print x and y classes
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
print(td_ys) #print coordinates from imported data
print(td_xs)

#create empty lists for agents and environment
agents = []
environment = []

# read in csv raster, convert str to float
f = open("in.txt", newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)

#set up csv data in to rows/grid
for row in reader:
    rowlist = []
    for value in row:
        rowlist.append(float(value))
    environment.append(rowlist)
f.close() #release the file now finished with it

#set up the figure
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1]) #add axes [left, bottom, width, height]

#ax.set_autoscale_on(False)

#Create agents
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    #give agents access to environment and other agents
    agents.append(agentframework.Agent(environment, agents, y, x))

#Allow code to carry on running when True
carry_on = True	

def update(frame_number):
    """
    Move agents and share data. Generate a frame for each iteration.
    
    Randomly shuffle the order in which agents move. Move agents a fixed
    number of times across the environment as an animation. Allow agents
    to take data in to their store and share with nearby agents. Stop
    when data store is full and write the content to .csv.
    
    Args:
        frame_number (int) -- A frame within the animation

    Returns:
        data_eaten (.csv) -- total data stored by agents after the final
            iteration
        Scatter plot and environmental data for each iteration.
    """
        
    fig.clear() #start animation
    global carry_on
    
    #Move each agent
    for j in range(num_of_iterations):
        for i in range(num_of_agents):
            random.shuffle(agents) #move agents in a different order each time
            agents[i].move()
            agents[i].eat()
            agents[i].share_with_neighbours(neighbourhood)
    
    #set to stop when data storage reaches max
    if agents[i].store > total_fill:
        carry_on = False #changes whether or not to carry on
        print("stopping condition. Final coordinates =")

        #write data_eaten.csv file with amount stored by agents
        s = 0
        for agent in agents:
            s += agent.store #sum agent store
        f3 = open('data_eaten.csv', 'a', newline = '')
        writer = csv.writer(f3, delimiter = ',')
        f3.write(str(s) + "\n") #write new entries to a new line
        f3.close() #realease file after use


    
    #plot the data to the figure
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.imshow(environment)
    for i in range (num_of_agents):
        #plot agents as a scatter graph
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
        print(agents[i].x, agents[i].y) #print coordinates after each iteration
    

            
#generator function to carry on the programme or stop it
def gen_function(b = [0]):
    """
    Determine whether to continue running the programme or to stop it.
    
    Requires no setup
    """
    a = 0
    global carry_on
    while (a < total_fill) & (carry_on) :
        yield a #return control and waits next call.
        a = a + 1

def run():
    """
    Compile frames and display model as animation.
    
    Requires no setup
    
    Returns:
        animation -- show agents moving within the environment
    
    """
    animation = matplotlib.animation.FuncAnimation(fig, update, repeat=False, 
                                                   frames=gen_function)
    canvas.show()

#create GUI
root = tkinter.Tk() 
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)


#write dataout.csv with new DEM information
f2 = open('dataout.csv', 'w', newline = '')
writer = csv.writer(f2, delimiter = ',') #, separates values to each cell
for row in environment:
    writer.writerow(row)
f2.close()


#Timing code - stop timer
end = getTimeMS()
print("time = " + str(end-start))

#wait for user response in GUI
tkinter.mainloop()
