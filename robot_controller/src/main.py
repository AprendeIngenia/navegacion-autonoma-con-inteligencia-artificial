# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Aprende e Ingenia                                            #
# 	Created:      3/24/2024, 9:51:26 PM                                        #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #
#vex:disable=repl

# Module pid
class PIDControl:
    def __init__(self, kp=30.0, ki=0.5, kd=10) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
        self.max_error_x = 640
        self.max_error_z = 22000
        self.max_speed = 100
        pass
    
    def pid_control(self, error, max_error_type) -> float:
        if error == 0:
           output = 0.0
           return output
        
        if max_error_type == 'x':
          error_normalized = self.normalize_error(error, self.max_error_x)
        else:
           error_normalized = self.normalize_error(error, self.max_error_z)
           
        self.integral += error_normalized
        derivative = error_normalized - self.prev_error
        output = self.kp * error_normalized + self.ki * self.integral + self.kd * derivative
        self.prev_error_x = error_normalized
        return output
    
    def normalize_error(self, error, max_error):
        return error / max_error

# Car control
# Library imports
from vex import *
import struct

# Brain should be defined by default
brain = Brain()
pid = PIDControl()

# Motor config
brain_inertial = Inertial()
left_drive = Motor(Ports.PORT1, True)
right_drive = Motor(Ports.PORT5, True)
drivetrain = SmartDrive(left_drive, right_drive, brain_inertial, 259.34, 320, 40, MM, 1)

brain.screen.print("Object control:")

def serial_monitor():
    try:
      s = open('/dev/serial1','rb')
    except:
      raise Exception('serial port not available')
    
    while True:
        #data= s.read(1)
        data= s.read(struct.calcsize("<ii"))
        unpacked = struct.unpack("<ii", data)

        error_x = unpacked[0]
        error_z = unpacked[1]

        # control signal pid
        control_x = pid.pid_control(error_x, 'x')
        control_x = min(control_x, 50)
        control_z = pid.pid_control(error_z, 'z')
        control_z = min(control_z, 50)

        # control motors
        right_drive.spin(FORWARD, control_x)
        left_drive.spin(FORWARD, control_x)

        if control_z != 0.0:
            right_drive.spin(FORWARD, control_z)
            left_drive.spin(REVERSE, control_z)
        
        brain.screen.print_at(control_x, x=5, y=40)
        brain.screen.print_at(control_z, x=5, y=80)
        
t1=Thread(serial_monitor)


        
