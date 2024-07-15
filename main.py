import sys

import pyautogui
import pyjoycon


class MyJoyCon(
    pyjoycon.GyroTrackingJoyCon,
    pyjoycon.ButtonEventJoyCon,
):
    pass


def connect_joycon(hand: str):
    joycon = None
    if hand == 'L':
        try:
            joycon_id = pyjoycon.get_L_id()
            joycon = MyJoyCon(*joycon_id)
        except ValueError:
            print('JoyConL Not found.')
    else:
        joycon_id = pyjoycon.get_R_id()
        joycon = MyJoyCon(*joycon_id)
    return joycon


def inputs_list(inputs: list):
    usable_inputs: list
    if inputs[0] == 0:
        usable_inputs = ["up", "right", "down", "left"]
    else:
        usable_inputs = ["a", "b", "y", "x"]

    return usable_inputs


def motion_controls(inputs: list):
    joycon = connect_joycon(inputs[0])

    toggle = True
    sensitivity = 1000

    inputs = inputs_list(inputs)

    while True:
        # Log joycon directional inputs
        print("\r" + "joycon pointer:", joycon.pointer, end='')

        if toggle:
            try:
                pyautogui.moveTo(1920 // 2 + joycon.pointer.x * sensitivity,
                                 1080 // 2 + joycon.pointer.y * -sensitivity, _pause=False)
            except AttributeError:
                print("Err, ignored")
                pass

        for event_type, status in joycon.events():
            if status == 1:
                # Click
                if event_type == inputs[0]:
                    pyautogui.click()
                # Finishes the program
                elif event_type == inputs[1]:
                    print('Exit')
                    sys.exit()
                # Reset position
                elif event_type == inputs[2]:
                    print('Pointer reset')
                    pyautogui.moveTo(1920 // 2, 1080 // 2)
                    joycon.reset_orientation()
                # Toggle off
                elif event_type == inputs[3]:
                    toggle = False if toggle else True
                    print(f"Tracking is turned {'on' if toggle else 'off'}")


if __name__ == '__main__':
    motion_controls([1, 0, 1, 2, 3])
