import ev3
import struct
import time


class EV3_BT_Controller:
    def __init__(self, motors):
        self.host = '00:16:53:4A:47:26'
        self.ev3 = ev3.EV3(protocol=ev3.BLUETOOTH, host=self.host)
        self.base_pos = (10,10)
        self.motors = motors
        self.base_pos = self.get_degrees_two_motors(self.motors)


    def move_single_motor(self, motor):
        ops = b''.join([
            ev3.opOutput_Speed,
            ev3.LCX(0),  # LAYER
            ev3.LCX(motor['port']),  # NOS
            ev3.LCX(motor['speed']),  # SPEED
        ])
        self.ev3.send_direct_cmd(ops)
        if 'duration' in motor:
            if motor['duration'] > 0:
                time.sleep(motor['duration'])
                self.stop()

    def move_two_motors(self, motors):
        ops = b''.join([
            ev3.opOutput_Speed,
            ev3.LCX(0),  # LAYER
            ev3.LCX(motors[0]['port']),  # NOS
            ev3.LCX(motors[0]['speed']),  # SPEED
            ev3.opOutput_Speed,
            ev3.LCX(0),  # LAYER
            ev3.LCX(motors[1]['port']),  # NOS
            ev3.LCX(motors[1]['speed']),  # SPEED
            ev3.opOutput_Start,
            ev3.LCX(0),  # LAYER
            ev3.LCX(motors[0]['port'] + motors[1]['port'])  # NOS
        ])
        self.ev3.send_direct_cmd(ops)
        if 'duration' in motors[0]:
            if motors[0]['duration'] > 0:
                time.sleep(motors[0]['duration'])
                self.stop()

    def stop(self) :#-> None:
        ops = b''.join([
            ev3.opOutput_Stop,
            ev3.LCX(0),  # LAYER
            ev3.LCX(ev3.PORT_A + ev3.PORT_D),  # NOS
            ev3.LCX(0)  # BRAKE
        ])
        self.ev3.send_direct_cmd(ops)

    def get_degrees_two_motors(self, motors):
        ops = b''.join([
            ev3.opInput_Device,
            ev3.READY_SI,
            ev3.LCX(0),  # LAYER
            ev3.port_motor_input(motors[0]['port']),  # NO
            ev3.LCX(7),  # TYPE
            ev3.LCX(0),  # MODE
            ev3.LCX(1),  # VALUES
            ev3.GVX(0),  # VALUE1
            ev3.opInput_Device,
            ev3.READY_RAW,
            ev3.LCX(0),  # LAYER
            ev3.port_motor_input(motors[1]['port']),  # NO
            ev3.LCX(7),  # TYPE
            ev3.LCX(0),  # MODE
            ev3.LCX(1),  # VALUES
            ev3.GVX(4)  # VALUE1
        ])
        reply = self.ev3.send_direct_cmd(ops, global_mem=8)
        (pos_0, pos_1) = struct.unpack('<fi', reply[5:])
        #pos_0 -= self.base_pos[0]
        #pos_1 -= self.base_pos[1]
        return pos_0, pos_1



    def get_degree_single_motor(self, motors, motor_num):
        ops = b''.join([
            ev3.opInput_Device,
            ev3.READY_SI,
            ev3.LCX(0),  # LAYER
            ev3.port_motor_input(motors[motor_num]['port']),  # NO
            ev3.LCX(7),  # TYPE
            ev3.LCX(0),  # MODE
            ev3.LCX(1),  # VALUES
            ev3.GVX(0),  # VALUE1
        ])
        reply = self.ev3.send_direct_cmd(ops, global_mem=8)
        pos = struct.unpack('<fi', reply[5:])
        print(pos)
        pos -= self.base_pos[motor_num]
        return pos
