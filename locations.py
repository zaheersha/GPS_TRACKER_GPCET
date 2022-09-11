import geopy.distance as geopy
import pyttsx3
import RPi.GPIO as gp
import serial, pynmea2, time
from RPLCD import CharLCD
gp.setwarnings(False)
lcd = CharLCD(numbering_mode=gp.BCM, pin_rs=26, pin_e=19, pins_data=[13,6,5,11])
framebuffer = ["",""]
engine = pyttsx3.init()
class Sound:
    @staticmethod
    def audio(text):
        engine.say(text)
        engine.runAndWait()
class Tracking:
    @staticmethod
    def track_location():
        while True:
            port="/dev/ttyAMA0"
            ser=serial.Serial(port, baudrate=9600, timeout=0.5)
            try:
                newdata=ser.readline().decode("utf-8")
                if newdata[0:6] == "$GPRMC":
                    newmsg=pynmea2.parse(newdata)
                    loc = (newmsg.latitude, newmsg.longitude)
                    break
            except:
                pass
        return loc
class LCD:
    @staticmethod
    def display(text, pos=(0, 0)):
        lcd.clear()
        lcd.cursor_pos=pos
        lcd.write_string(text)
    @staticmethod
    def clear_the_screen():
        lcd.clear()
        lcd.home()
class Locations(LCD, Tracking):

    enterance_left_enterance = (15.79817913188578, 78.07837122128761)
    enterance_right_enterance = (15.798162745540536, 78.07844466147382)
    #
    # # block1
    block1_enterance = (15.797255349596949, 78.07759424540234)
    block1_back_enterance = (15.797009553155037, 78.07749951820676)
    # # library
    library_enterance = (15.796982925189564, 78.07771345266227)
    #
    # # block2
    block2_left_enterance = (15.796705379637835, 78.07686835832361)
    block2_right_enterance = (15.796866171750267, 78.07689283838569)
    #
    # # canteen
    canteen_enterance = (15.797206473501456, 78.07699258260875)
    #
    # # block3
    block3_enterance = (15.796361546778973, 78.07714159169284)
    #
    bikes_parking = (15.797554322919448, 78.07826399981849)
    bikes_parking2 = (15.797151537252812, 78.07814041263727)

    #indoor stadium
    indoor_stadium = (15.79663456027133, 78.07801350348288)
    #
    # # rcew
    rcew_enterance = (15.795747052403074, 78.07757797541669)
    #
    # # rcew
    rcew_collage = (15.79523702064963, 78.07717565088527)
    # girls_hostel
    girls_hostel_enterance = (15.795503302441732, 78.07680525689258)


    def __init__(self):
        location = Tracking.track_location()
        self.distance_to_left_enterance = self.distance(location, self.enterance_left_enterance)
        self.distance_to_right_enterance = self.distance(location, self.enterance_right_enterance)

        # block1
        self.distance_block1_front_enterance = self.distance(location, self.block1_enterance)
        self.distance_block1_back_enterance = self.distance(location, self.block1_back_enterance)

        # library
        self.distance_to_library = self.distance(location, self.library_enterance)

        # block2
        self.distance_to_block2_left_enterance = self.distance(location, self.block2_left_enterance)
        self.distance_to_block2_right_enterance = self.distance(location, self.block2_right_enterance)

        # block3
        self.distance_to_block3_enterance = self.distance(location, self.block3_enterance)

        # canteen
        self.distance_to_canteen = self.distance(location, self.canteen_enterance)
        #bikes_parking
        self.distance_to_bikes_parking = self.distance(location, self.bikes_parking)
        self.distance_to_bikes_parking2 = self.distance(location, self.bikes_parking2)
        # rcew
        self.distance_to_rcew = self.distance(location, self.rcew_enterance)
        #indoor_stadium
        self.distance_to_indoor_stadium = self.distance(location,self.indoor_stadium)

        self.distance_to_rcew_college = self.distance(location, self.rcew_collage)
        self.distance_to_girls_hostel = self.distance(location, self.girls_hostel_enterance)

    @staticmethod
    def distance(c1, c2):
        return geopy.distance(c1, c2)
    def compare(dis):
        if dis.distance_to_left_enterance < 0.03 or dis.distance_to_right_enterance < 0.03:
            result = "ENTERED GPCET"

        elif dis.distance_to_library < 0.015:
            result = "REACHED LIBRARY"
        elif dis.distance_to_canteen< 0.020:
            result = "REACHED CANTEEN"
        elif dis.distance_block1_front_enterance < 0.025 or dis.distance_block1_back_enterance < 0.015:
            result = "BLOCK 1 REACHED"
        elif dis.distance_to_block2_left_enterance < 0.020 or dis.distance_to_right_enterance < 0.02:
            result = "BLOCK 2 REACHED"
        elif dis.distance_to_block3_enterance < 0.025:
            result = "BLOCK 3 REACHED"
        elif dis.distance_to_bikes_parking < 0.030 and dis.distance_to_bikes_parking2 < 0.030 :
            result = "BIKE'S PARKING"
        elif dis.distance_to_indoor_stadium < 0.03:
            result = "INDOOR STADIUM"
        elif dis.distance_to_rcew < 0.03:
            result = "Entered R C E W"
        elif dis.distance_to_rcew_college < 0.03:
            result = "REACHED R C E W"
        elif dis.distance_to_girls_hostel < 0.03:
            result = "GIRLS HOSTEL"
        else:
            result = "ON THE WAY"
        dis.display(result)
       
        return result


    
    
