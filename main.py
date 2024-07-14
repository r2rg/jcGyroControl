import sys
import pyautogui

import pyjoycon
import time


class MyJoyCon(
    pyjoycon.GyroTrackingJoyCon,
    pyjoycon.ButtonEventJoyCon,
):
    pass


def motion_controls(inputs: list):
    joycon_id = pyjoycon.get_L_id()
    joycon = MyJoyCon(*joycon_id)

    #print('Input sensitivity: ')
    sensitivity = 500 #int(input())

    while True:
        # Log joycon directional inputs
        print("\r" + "joycon pointer:", joycon.pointer, end='')

        try:
            pyautogui.moveTo(1920 // 2 + joycon.pointer.x * sensitivity,
                             1080 // 2 + joycon.pointer.y * -sensitivity, _pause=False)
        except AttributeError:
            print("Err, ignored")
            pass

        for event_type, status in joycon.events():
            # Resets cursor position to the center of the screen and reset JC orientation
            if event_type == inputs[0]:
                pyautogui.moveTo(1920 // 2, 1080 // 2)
                joycon.reset_orientation()
            # Finishes the program
            elif event_type == inputs[1]:
                sys.exit()
            # Adds 10% to current sensitivity
            elif event_type == inputs[2]:
                sensitivity += sensitivity / 10
                print(sensitivity)

        #time.sleep(0.001)


if __name__ == "__main__":
    motion_controls(['up', 'right', 'down'])
