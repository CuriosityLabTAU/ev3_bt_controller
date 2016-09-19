
#!/usr/bin/env python3

import ev3, struct, time

my_ev3 = ev3.EV3(protocol=ev3.BLUETOOTH, host='00:16:53:4A:47:26')

def change_color(color) -> bytes:
    return b''.join([
        ev3.opUI_Write,
        ev3.LED,
        color
    ])

def play_sound(vol: int, freq: int, dur:int) -> bytes:
    return b''.join([
        ev3.opSound,
        ev3.TONE,
        ev3.LCX(vol),
        ev3.LCX(freq),
        ev3.LCX(dur)
    ])

def ready() -> None:
    ops = change_color(ev3.LED_RED)
    my_ev3.send_direct_cmd(ops)
    time.sleep(3)

def steady() -> None:
    ops_color = change_color(ev3.LED_ORANGE)
    ops_sound = play_sound(1, 200, 60)
    my_ev3.send_direct_cmd(ops_color + ops_sound)
    time.sleep(0.25)
    for i in range(3):
        my_ev3.send_direct_cmd(ops_sound)
        time.sleep(0.25)

def go() -> None:
    ops_clear = b''.join([
        ev3.opInput_Device,
        ev3.CLR_CHANGES,
        ev3.LCX(0),          # LAYER
        ev3.LCX(1)           # NO
    ])
    ops_color = change_color(ev3.LED_GREEN_FLASH)
    ops_sound = play_sound(10, 200, 100)
    my_ev3.send_direct_cmd(ops_clear + ops_color + ops_sound)
    time.sleep(5)

def stop() -> None:
    ops_read = b''.join([
        ev3.opInput_Device,
        ev3.READY_SI,
        ev3.LCX(0),          # LAYER
        ev3.LCX(1),          # NO
        ev3.LCX(16),         # TYPE - EV3-Touch
        ev3.LCX(0),          # MODE - Touch
        ev3.LCX(1),          # VALUES
        ev3.GVX(0),          # VALUE1
        ev3.opInput_Device,
        ev3.READY_SI,
        ev3.LCX(0),          # LAYER
        ev3.LCX(1),          # NO
        ev3.LCX(16),         # TYPE - EV3-Touch
        ev3.LCX(1),          # MODE - Bump
        ev3.LCX(1),          # VALUES
        ev3.GVX(4)           # VALUE1
    ])
    ops_sound = play_sound(10, 200, 100)
    reply = my_ev3.send_direct_cmd(ops_sound + ops_read, global_mem=8)
    (touched, bumps) = struct.unpack('<ff', reply[5:])
    if touched == 1:
        bumps += 0.5
    print(bumps, "bumps")

for i in range(3):
    ready()
    steady()
    go()
    stop()
ops_color = change_color(ev3.LED_GREEN)
my_ev3.send_direct_cmd(ops_color)
print("**** Game over ****")