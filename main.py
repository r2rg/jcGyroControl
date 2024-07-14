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
    toggle = False
    running = True
    sensitivity = 500

    while running:
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
                    time.sleep(0.02)
                # Finishes the program
                elif event_type == inputs[1]:
                    print('Exit')
                    running = False if running else True
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
    motion_controls(['up', 'right', 'down', 'left'])
