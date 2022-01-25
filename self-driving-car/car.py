from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import time
import board

class Car:
    def __init__(self):
        print("Hi, I am the car.\n")
        print("Starting engine...")

        self.kit = MotorKit(i2c=board.I2C())

        # while True:
        #     self.timer.tick ()
        #     self.input ()
        #     self.sweep ()
        #     self.output ()
        #     tm.sleep (0.02)


    def drive(self):
        self.kit.motor3.throttle = 0.5
        time.sleep(8)
        self.kit.motor3.throttle = 0

    def steer(self):
        for i in range(1000):
            self.kit.stepper1.onestep(style=stepper.DOUBLE)
            time.sleep(0.01)

car = Car()
car.drive()
# car.steer()