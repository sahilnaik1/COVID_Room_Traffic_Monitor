import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

#LIVE VISITS
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(2,1,1)
#ax2 = fig.add_subplot(2,1,2)

def animateLive(i):
    infile = open('test.txt','r')
    graph_data = infile.read()
    lines = graph_data.split('\n')
    xs = [0,1,2,3,4,5]
    ys = [0,0,0,0,0,0]
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            currentY = ys[int(x)]
            currentY += int(y)
            #xs.append(float(x))
            #ys.append(float(y))
            ys[int(x)] = currentY
            
    ax1.clear()
    #ax1.plot(xs, ys)
    ax1.bar(xs, ys, label="Live", color= 'c')
    plt.xlabel('Hours')
    plt.ylabel('            Visits')
    plt.legend()
    infile.close()
    
ani1 = animation.FuncAnimation(fig1, animateLive, interval=1000)



#COVID HALF LIFE
fig2 = plt.figure(2)
ax3 = fig2.add_subplot(1,1,1)

def animateHalfLife(i):
    infile = open('test2.txt', 'r')
    graph_data = infile.read()
    lines = graph_data.split('\n')
    Time = []
    COVIDHalfLife = []
    for line in lines:
        if (len(line) > 1):
            x, y, z = line.split(',')
            current_temperature = int(z)
            Time.append(int(x))
            COVIDHalfLife.append(int(y))
    ax3.clear()
    ax3.plot(Time, COVIDHalfLife, label = "Covid half life", color= 'r')
    #fig2.legend()
    plt.xlabel('Time')
    plt.ylabel("Covid Half Life")
    plt.title("Current Room Temperature: " + str(current_temperature) + " °F")
    infile.close()
ani2 = animation.FuncAnimation(fig2, animateHalfLife, interval = 1000)       
plt.show()



