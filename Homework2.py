
import math

class ROS:
    def __init__(self, x, y, angle = 0, velocity = 1):
        """
        angle: Counterclockwise angle from x-axis to robot direction.
        velocity: Linear motion speed, default initialized to 1.
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = velocity
        self.engine_status = False
        self.power_status = False
        print(f'Initializing finished. Coordinate:({self.x},{self.y}). Angle:{self.angle}. Velocity:{self.velocity}')

    def diesel_engine(self, status):
        self.engine_status = status

        if status:
            print("Diesel engine ON.")
        else:
            print("Diesel engine OFF.")

    def power_switch(self, operation):
        if operation == True or operation == False:
            self.power_status = operation

            if operation:
                print("Power ON.")
            else:
                print("Power OFF.")

        elif operation =="check":        
            print('Checkin status:')
            self.diesel_engine(self.engine_status)
            self.power_switch(self.power_status)
            print('\n')

    def robot(self, operation, parameter = 0):
        """
        operation: 'forward'    /'rotation'       /'stop'
        parameter: Forward time /Rotation angle   /None

        """

        if self.engine_status and self.power_status:

            if operation == 'forward':
                self.x = self.x + parameter * self.velocity * math.cos(self.angle / 180 * math.pi)
                self.y = self.y + parameter * self.velocity * math.sin(self.angle / 180 * math.pi)
                print(f'Moving...Time:{parameter}')

            elif operation == 'rotate':
                self.angle = self.angle + parameter
                print(f'Rotating...Angle:{self.angle}')

            elif operation == 'stop':
                print(f'The robot stops. Coordinate:({self.x},{self.y}). Angle:{self.angle}\n')

            else :
                print('Invalid operation!\n')

        else:
            print('Operation failed.\n')
            self.power_switch("check")

if __name__ == '__main__':
    rob1 = ROS(0,0)
    rob1.diesel_engine(True)
    rob1.robot('forward',10)
    
    rob2 = ROS(0,0)
    rob2.diesel_engine(True)
    rob2.power_switch(True)

    rob2.robot('rotate',45)
    rob2.robot('forward',10)
    rob2.robot('stop')

    rob2.robot('backward')