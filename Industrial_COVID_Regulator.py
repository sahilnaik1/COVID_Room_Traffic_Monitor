import serial
from datetime import datetime
import pandas as pd

MAX_RANGE = 180
INIT_ANGLE = 0

def main():
  ser = serial.Serial('COM3', 9600)
  time.sleep(2)
  calibrated = {}
  
  visits_df = pd.DataFrame(columns=['Visits', 'Hour', 'Day', 'Month', 'Year'])
  chl_df = pd.DataFrame(columns=['CHL', 'Hour'])

  # Calibrate initial distances for comparison at each sweep
  while(True): #Add a condition to kill the session
    	b = ser.readline()						# read a byte string
    	string_n = b.decode()  					# decode byte string into Unicode  
    	string = string_n.rstrip() 				# remove \n and \r
        angle, distance = string.split(",")
  		if (angle <= INIT_ANGLE + MAX_RANGE):
    		calibrated.append(distance)
        else:
          break
          
  visits = 0
  temp = 0
  humidity = 0
  # Calculate difference in distance between angle measurement & calibrated value
  while(True): #Add a condition to kill the session
    	b = ser.readline()						# read a byte string
    	string_n = b.decode()  					# decode byte string into Unicode  
    	string = string_n.rstrip() 				# remove \n and \r
        if (string[0] == "T"):
            temp, humidity = string.split(",")
            now = datetime.now()
            
            temp = float(temp)
            humidity = float(humidity)
            chl = 32.43 - 0.62*temp - 0.15*humidity #equation according to DHS // chl is Covid19 Half Life estimates in hours
            
            
            new_row = {'CHL': chl, 'Hour': now.hour}
            
            chl_df = chl_df.append(new_row, ignore_index=True)
            
            
        elif (string[0] == "B"):
            break
        angle, distance = string.split(",")
        if (abs(distance - calibrated.get(angle)) < 0.05 * calibrated.get(angle)): #threshold of 5% to minimalize variations in the environment
            visits += 1
            now = datetime.now()
            new_row = {'Visits':visits, 'Hour':now.hour, 'Day':now.day, 'Month':now.month, 'Year':now.year} #would give hour and a date num
            visits_df = visits_df.append(new_row, ignore_index=True)

  ser.close()
  visits_df.to_csv(index=False) #Writes data to csv file
  chl_df.to_csv(index=False)
    
  
if __name__=='__main__':
  main()
