import math, time
import numpy as np
import paho.mqtt.client as mqtt
import tinyik
import matplotlib.pyplot as plt


d=3.8

arm = tinyik.Actuator(['z', [3.8, 0., 0.], 'z', [3.8, 0., 0.]])

broker_address=''
def callback(source,user,message):
    print(message.payload.decode())
client = mqtt.Client("kinematics")
client.connect(broker_address)
client.on_message = callback
client.loop_start()
client.subscribe('ME035')
client.on_message = callback

x = [1.9, 2.09, 2.28, 2.47, 2.66, 2.85, 3.04, 3.23, 3.42, 3.61, 3.8, 3.99, 4.18, 4.37, 4.56, 4.75, 4.94, 5.13, 5.32, 5.51, 5.7, 5.51, 5.32, 5.13, 4.94, 4.75, 4.56, 4.37, 4.18, 3.99, 3.8, 3.61, 3.42, 3.23, 3.04, 2.85, 2.66, 2.47, 2.28, 2.09, 1.9]

y = [0, 0.828190799, 1.14, 1.356871401, 1.52, 1.645448267, 1.741378764, 1.812484483, 1.861612205, 1.890476131, 1.9, 1.890476131, 1.861612205, 1.812484483, 1.741378764, 1.645448267, 1.52, 1.356871401, 1.14, 0.828190799, 0, -0.828190799, -1.14, -1.356871401, -1.52, -1.645448267, -1.741378764, -1.812484483, -1.861612205, -1.890476131, -1.9, -1.890476131, -1.861612205, -1.812484483, -1.741378764, -1.645448267, -1.52, -1.356871401, -1.14, -0.828190799, 0]

plt.plot(np.array(x), np.array(y))
plt.show()

print(type(x))
for i in range(len(x)):
    angle2=-math.acos(((x[i]**2)+(y[i]**2) - 2*d**2)/(2*d**2))
    angle1=-math.atan2(y[i],x[i])+math.atan2((d*math.sin(angle2)),(d+d*math.cos(angle2)))
    message='('+str(np.rad2deg(angle1))+','+str(np.rad2deg(angle2))+')'
    print(message)
    #client.publish("listen2",np.rad2deg(angle2))
    #client.publish("listen2",np.rad2deg(angle1))
    #client.publish("ME035",message)
    arm.angles = [angle1, angle2]
    tinyik.visualize(arm)
    time.sleep(.1)
client.loop_stop()
