import math
import time
import serial
import string
import pynmea2
import RPi.GPIO as gpio
import smtplib,ssl    
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders
import os
import goocal
import datetime
import pickle
import sys

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
BUZZ=18
red=3
green=4
wrong=0
gpio.setup(BUZZ,gpio.OUT)
gpio.setup(red,gpio.OUT)
gpio.setup(green,gpio.OUT)
port = "/dev/ttyUSB0" # the serial port to which the pi is connected.
 
#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

def sms(lata,lnga):
    # Enable Serial Communication
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
 
    # Transmitting AT Commands to the Modem
    # '\r\n' indicates the Enter key
    port.write('AT'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('ATE0'+'\r\n')      # Disable the Echo
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
    rcv = port.read(10)
    print rcv
    time.sleep(1)
    # Sending a message to a particular Number
    port.write('AT+CMGS="+919000550200"'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(1)
    #lcd.message(str(gps))
    #time.sleep(3)
    #lcd.clear()
    message='ALERT:Child is out of his way find here '+'http://www.google.com/maps/place/'+str(lata)+','+str(lnga)

    print message
    port.write(message+'\r\n')  # Message
    rcv = port.read(10)
    print rcv
    
    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv

def police(ps,lata,lnga):
    # Enable Serial Communication
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
 
    # Transmitting AT Commands to the Modem
    # '\r\n' indicates the Enter key
    port.write('AT'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('ATE0'+'\r\n')      # Disable the Echo
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
    rcv = port.read(10)
    print rcv
    time.sleep(1)
    # Sending a message to a particular Number
    port.write('AT+CMGS="+919000550200"'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(1)
    #lcd.message(str(gps))
    #time.sleep(3)
    #lcd.clear()
    message='ALERT:Child is out of his way'+'Message for'+ps+'http://www.google.com/maps/place/'+str(lata)+','+str(lnga)

    print message
    port.write(message+'\r\n')  # Message
    rcv = port.read(10)
    print rcv
    
    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv
 
def GPS():
    try:
        data = ser.readline()
    except:
	print "loading" 
	#wait for the serial port to churn out data
 
    if data[0:6] == '$GPGGA': # the long and lat data are always contained in the GPGGA string of the NMEA data
 
        msg = pynmea2.parse(data)
 
	#parse the latitude and print
        latval = msg.latitude
	concatlat = "lat:" + str(latval)
	#print concatlat
	longval = msg.longitude
	concatlong = "long:"+ str(longval)
	#print concatlong
           
	time.sleep(0.5)
	return [latval,longval]

def send_an_email():
    os.system('fswebcam --no-banner -r 640x480 image.jpg')
    toaddr = 'mprashanthi397@gmail.com'      # To id 
    me = 'Unitracksys@gmail.com'          # your id
    subject = "Student Image"              # Subject
  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
    #msg.attach(MIMEText(text))  
  
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("image.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')   # File name and format name
    msg.attach(part)  
  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'Unitracksys@gmail.com', password = 'pgproject123')  # User id & password
       #s.send_message(msg)  
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()
       print "Email Sent"
    #except:  
    #   print ("Error: unable to send email")    
    except SMTPException as error:  
          print "Error"                # Exception
  


def getPathLength(lat1,lng1,lat2,lng2):
    '''calculates the distance between two lat, long coordinate pairs'''
    R = 6371000 # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    deltaLat = math.radians((lat2-lat1))
    deltaLng = math.radians((lng2-lng1))
    a = math.sin(deltaLat/2) * math.sin(deltaLat/2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(deltaLng/2) * math.sin(deltaLng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def getDestinationLatLong(lat,lng,azimuth,distance):
    '''returns the lat an long of destination point 
    given the start lat, long, aziuth, and distance'''
    R = 6378.1 #Radius of the Earth in km
    brng = math.radians(azimuth) #Bearing is degrees converted to radians.
    d = distance/1000 #Distance m converted to km
    lat1 = math.radians(lat) #Current dd lat point converted to radians
    lon1 = math.radians(lng) #Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1)* math.sin(d/R)* math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R)* math.cos(lat1), math.cos(d/R)- math.sin(lat1)* math.sin(lat2))
    #convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return[lat2, lon2]

def calculateBearing(lat1,lng1,lat2,lng2):
    '''calculates the azimuth in degrees from start point to end point'''
    startLat = math.radians(lat1)
    startLong = math.radians(lng1)
    endLat = math.radians(lat2)
    endLong = math.radians(lng2)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
         if dLong > 0.0:
             dLong = -(2.0 * math.pi - dLong)
         else:
             dLong = (2.0 * math.pi + dLong)
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

def main(interval,azimuth,lat1,lng1,lat2,lng2):
    '''returns every coordinate pair inbetween two coordinate 
    pairs given the desired interval'''

    d = getPathLength(lat1,lng1,lat2,lng2)
    remainder, dist = math.modf((d / interval))
    counter = float(interval)
    coords = []
    coords.append([lat1,lng1])
    for distance in range(0,int(dist)):
        coord = getDestinationLatLong(lat1,lng1,azimuth,counter)
        counter = counter + float(interval)
        coords.append(coord)
    coords.append([lat2,lng2])
    print d,'meters'
    time.sleep(2)
    return coords

if __name__ == "__main__":
    #point interval in meters
    interval = 1
    #direction of line in degrees
    #start point
    #lat1 = float(raw_input('Enter the source latitude: '))
    #lng1 = float(raw_input('Enter the 1st longitude: '))
    starttime=int(time.strftime("%H"))
    print "Now the Time is",starttime,"Hours"
    if starttime>8 and starttime<15:
        lat1 = 17.49686873794865        #Home
        lng1 = 78.39165222926943
        lat2 = 17.4315385               #to School
        lng2 = 78.4467634
    elif starttime>15 and starttime<18:
        lat1 = 17.4315385               #School
        lng1 = 78.4467634
        lat2 = 17.49686873794865        #Home
        lng2 = 78.39165222926943
    elif starttime>17 and starttime<21:
        lat1 = 17.49686873794865        #Home
        lng1 = 78.39165222926943
        lat2 = 17.496431880125385       #Tution
        lng2 = 78.36161730834738
    elif starttime>21 and starttime<23:
        lat1 = 17.496431880125385       #Tution
        lng1 = 78.36161730834738
        lat2 = 17.49686873794865        #Home
        lng2 = 78.39165222926943
    else:
        print 'Shedule Not Started have a nice Day'
        sys.exit()
    
        
    #end point
    #lat2 = 16.437462
    #lng2 = 78.448288
    #lat2=float(raw_input('enter dest lat'))
    #lng2=float(raw_input('enter dest lng'))
    azimuth = calculateBearing(lat1,lng1,lat2,lng2)
    #print (azimuth)
    coords = main(interval,azimuth,lat1,lng1,lat2,lng2)
    final_dist_coords=[]
    #print coords
    for gps_data in coords:
            lat_gps_data='%.5f'%gps_data[0]
            lng_gps_data='%.5f'%gps_data[1]
            final_dist_coords.append([lat_gps_data,lng_gps_data])
    print final_dist_coords
    print len(final_dist_coords)

    pickle_h2s = open("h2s.pickle","rb")
    h2s_coords = pickle.load(pickle_h2s)
    pickle_h2t = open("h2t.pickle","rb")
    h2t_coords = pickle.load(pickle_h2t)
    datas=goocal.calend()

    dataa=str(datetime.datetime.now())
    pre_date=dataa[:10]
    print(datas)

    value="nothing"
    for a in datas:
        if pre_date in a[0]:
            if a[1]=='school':
                value='school'
            else:
                value='holiday'
        else:
            pass

    if value=='school':
        print 'The Shedule is Set for School Routine Go Safe'
    elif value=='holiday':
        print 'Today Holiday Enjoy Your Holiday'
        sys.exit()
    else:
        print 'Today There is No Shedule Today Looks Like Its a Holiday'
        sys.exit()
    
                

while True:
    
    gpscoords1=[16.44041,78.44797] #right coordinates
    gpscoords=[15.23540,77.80252] #wrong coordinates
    #gpscoords=[16.24917,77.81031]
    #gpscoords=gps()
    for i in range(10):
        gps=GPS()
        if gps!=None and gps!=[0.0,0.0]:
            gpscoords=gps()
        else:
            gpscoords=[17.49643, 78.36188]
    try:
        if gpscoords!=None and wrong<15:
            lat_gpscoords='%.5f'%gpscoords[0]
            lng_gpscoords='%.5f'%gpscoords[1]
            final_gpscoords=[str(lat_gpscoords),str(lng_gpscoords)]
            print 'latitude:',lat_gpscoords
            print 'longitude:',lng_gpscoords
            
            time.sleep(0.5)
            if final_gpscoords in final_dist_coords:
                gpio.output(BUZZ,gpio.LOW)
                gpio.output(red,gpio.LOW)
                gpio.output(green,gpio.HIGH)
                print 'You are going perfect :positive progress'
                time.sleep(0.5)
                wrong=0
            else:
                gpio.output(BUZZ,gpio.HIGH)
                time.sleep(3)
                gpio.output(BUZZ,gpio.LOW)
                gpio.output(red,gpio.HIGH)
                gpio.output(green,gpio.LOW)
                print 'WARNING:WRONG DIRECTION : negative progress'
                time.sleep(0.5)
                wrong+=1
                if wrong>5:
                    #sms(lat_gpscoords,lng_gpscoords)
                    lat_gpscoords='%.4f'%gpscoords[0]
                    lng_gpscoords='%.4f'%gpscoords[1]
                    final_gpscoords=[str(lat_gpscoords),str(lng_gpscoords)]
                    if final_gpscoords in h2s_coords[0:932]:
                        print "Sending message to the Police Station-1"
                        police('Police Station1',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[932:1864]:
                        print "Sending message to the Police Station-2"
                        police('Police Station2',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[1864:2796]:
                        print "Sending message to the Police Station-3"
                        police('Police Station3',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[2796:3278]:
                        print "Sending message to the Police Station-4"
                        police('Police Station4',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[3278:4660]:
                        print "Sending message to the Police Station-5"
                        police('Police Station5',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[4660:5592]:
                        print "Sending message to the Police Station-6"
                        police('Police Station6',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[5592:6524]:
                        print "Sending message to the Police Station-7"
                        police('Police Station7',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[6524:7456]:
                        print "Sending message to the Police Station-8"
                        police('Police Station8',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[7456:8388]:
                        print "Sending message to the Police Station-9"
                        police('Police Station9',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2s_coords[8388:]:
                        print "Sending message to the Police Station-10"
                        police('Police Station10',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[0:318]:
                        print "Sending message to the Police Station-11"
                        police('Police Station11',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[318:636]:
                        print "Sending message to the Police Station-12"
                        police('Police Station12',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[636:954]:
                        print "Sending message to the Police Station-13"
                        police('Police Station13',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[954:1272]:
                        print "Sending message to the Police Station-14"
                        police('Police Station14',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[1272:1590]:
                        print "Sending message to the Police Station-15"
                        police('Police Station15',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[1590:1908]:
                        print "Sending message to the Police Station-16"
                        police('Police Station16',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[1908:2226]:
                        print "Sending message to the Police Station-17"
                        police('Police Station17',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[2226:2544]:
                        print "Sending message to the Police Station-18"
                        police('Police Station18',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[2544:2862]:
                        print "Sending message to the Police Station-19"
                        police('Police Station19',lat_gpscoords,lng_gpscoords)
                    elif final_gpscoords in h2t_coords[2862:]:
                        print "Sending message to the Police Station-20"
                        police('Police Station20',lat_gpscoords,lng_gpscoords)
                    else:
                        print "Sending message to the Police Station"
                        police('Police Station',lat_gpscoords,lng_gpscoords)
                    send_an_email()
                    wrong=0

        if gpscoords1!=None and wrong>=15:
            lat_gpscoords='%.5f'%gpscoords1[0]
            lng_gpscoords='%.5f'%gpscoords1[1]
            final_gpscoords=[str(lat_gpscoords),str(lng_gpscoords)]
            print 'latitude:',lat_gpscoords
            print 'longitude:',lng_gpscoords
            
            time.sleep(0.5)
            if final_gpscoords in final_dist_coords:
                gpio.output(BUZZ,gpio.LOW)
                gpio.output(red,gpio.LOW)
                gpio.output(green,gpio.HIGH)
                print 'You are going perfect :positive progress'
                time.sleep(0.5)
                
          
               
                    
                
    except KeyboardInterrupt:
        print 'The System Shutdown'
        sys.exit()
                
            
            
    
