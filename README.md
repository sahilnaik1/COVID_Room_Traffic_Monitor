# COVID Room Traffic Monitor

An ultrasonic sound-based movement detection system that can be deployed in areas with small spaces to study foot traffic and congestion over periods of time.

## Installation

### Components
- Arduino UNO 
- DHT11 digital temperature and humidity sensor
- Breadboard Button
- Jumper cables
- Servo Motor
- HC-SR04 Ultrasonic Sensor

### Schematic
![Schematic](images/schematic.jpg)

To build the circuit, follow [this guide](http://howtomechatronics.com/projects/arduino-radar-project/) that the project was based on.

## Usage

Load the Arduino code into an Arduino UNO. Immediately after the code is loaded, run the Python script.
```python
python Industrial_COVID_Regulator.py
```

If you run into any issues, your best bet is to re-upload the code to the Arduino and run the Python script again. Currently, the code outputs all the degrees of its range scanned for the calibration stage. What then follows is any change detected by the sensor in the format:

`degree:measurement:calibration`
