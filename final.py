from locations import *
import time
lcd_ = LCD()
lcd_.clear_the_screen()
last_location = "System Rebooted"

Sound.audio(last_location)
lcd_.display(last_location)
time.sleep(2)
lcd_.display("Welcome", pos=(0, 4))
Sound.audio("Welcome")
lcd.home()
while True:
   coordinates = Tracking.track_location()
   location = Locations().compare()
   if coordinates == (0.0, 0.0):
        lcd_.display("Connecting...")
   if location != last_location:
        Sound.audio(location)
        lcd_.display(location)
        last_location=location
    
