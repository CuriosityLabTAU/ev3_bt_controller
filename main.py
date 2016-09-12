from ev3_bt_controller import *

motors = [
    {
        'port': 1,
        'speed': 0,
        'duration': 1
    },
    {
        'port': 8,
        'speed': 10,
        'duration': 1
    }
]
c = EV3_BT_Controller(motors)

for i in range(2):
    c.move_two_motors(motors)
    print(c.get_degrees_two_motors(motors))

motor = [
    {
        'port': 1,
        'speed': 100,
        'duration': 1
    }
]
c1 = EV3_BT_Controller(motor)

for i in range(2):
    c1.move_single_motor(motor)
    print(c1.get_degree_single_motor(motor))