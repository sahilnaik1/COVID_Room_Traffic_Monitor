import time
import serial
from datetime import datetime
import pandas as pd

MAX_ANGLE = 110 # degrees
INIT_ANGLE = 15 # degrees
LIMIT_RANGE = 40 # cm

def main():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)
    calibrated = {}

    visits_df = pd.DataFrame(
        columns=[
            'Visits',
            'Hour',
            'Day',
            'Month',
            'Year'])
    chl_df = pd.DataFrame(columns=['CHL', 'Hour'])

    print("####### CALIBRATE #######")
    print("ANGLE : DISTANCE")
    # Calibrate initial distances for comparison at each sweep
    while(True):  # Add a condition to kill the session
        b = ser.readline()					# read a byte string
        string_n = b.decode()   				# decode byte string into Unicode
        string = string_n.rstrip()                              # remove \n and \r
        if (string.isspace()):
            pass
        elif (string == ""):
            pass
        elif (not string):
            pass
        elif (string[0] == 'T'):
            pass
        else:
            angle, distance = string.split(",")
            if (len(calibrated) < MAX_ANGLE-INIT_ANGLE+1):
                if (float(distance) > LIMIT_RANGE): # LIMIT CALIBRATION RANGE
                    distance = LIMIT_RANGE
                data={int(angle):float(distance)}
                calibrated.update(data)
                print(str(angle) + " degrees : " + str(distance) + "cm")
            else:
                break
    visits = 0
    temp = 0
    humidity = 0
    # Calculate difference in distance between angle measurement & calibrated
    # value
    print("####### DETECT #######")
    print("ANGLE : CALIBRATE DISTANCE - DISTANCE")
    while(True):  # Add a condition to kill the session
        b = ser.readline()						# read a byte string
        string_n = b.decode()  					        # decode byte string into Unicode
        string = string_n.rstrip() 				        # remove \n and \r
        if (string[0] == "T"):
            temp, humidity = string.split(",")
            now = datetime.now()

            temp = float(temp[1:])
            humidity = float(humidity)
            # equation according to DHS // chl is Covid19 Half Life estimates
            # in hours
            chl = 32.43 - 0.62 * temp - 0.15 * humidity

            new_row = {'CHL': chl, 'Hour': now.hour}

            chl_df = chl_df.append(new_row, ignore_index=True)
            pass
        elif (string[0] == "B"): # Button Press to Exit
            break
        angle, distance = string.split(",")
        try:
            if (float(distance) > LIMIT_RANGE):
                distance = LIMIT_RANGE
            if (abs(float(distance) - calibrated.get(int(angle))) > 0.15 * calibrated.get(int(angle))):  # threshold of 15% to minimalize effects of variations in the environment
                print(str(angle) + " degrees : " + str(float(calibrated.get(int(angle))) - float(distance)) + " cm")
                visits += 1
                now = datetime.now()
                new_row = {
                    'Visits': visits,
                    'Hour': now.hour,
                    'Day': now.day,
                    'Month': now.month,
                    'Year': now.year}  # would give hour and a date num
                visits_df = visits_df.append(new_row, ignore_index=True)
        except ValueError:
            continue
    
    print(visits_df)
    print(chl_df)

    ser.close()
    visits_df.to_csv(index=False)  # Writes data to csv file
    chl_df.to_csv(index=False)


if __name__ == '__main__':
    main()
