from pynput.mouse import Button, Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import threading
import math

keyboard = KeyboardController()
mouse = MouseController()

start_loc: list[2]|None = None
minimum_movement_for_change = 20
one_volume_change = 50
scroll_lock = threading.Lock()
thumb_lock = threading.Lock()

def press_key(key: Key):
    keyboard.press(key)
    keyboard.release(key)

def on_click(x, y, button, pressed):
    global start_loc
    if Button.button10 == button:
        if pressed:
            thumb_lock.acquire()
            start_loc = [x, y]
        else: # released
            thumb_lock.release()
            if not scroll_lock.locked():
                movement_vector = [start_loc[0] - x, start_loc[1] - y]
                movement_length = math.hypot(movement_vector[0], movement_vector[1])
                if movement_length < minimum_movement_for_change:  # To make single clicks easier
                    press_key(Key.media_play_pause)
                elif abs(movement_vector[0]) > abs(movement_vector[1]):  # Movement is horizontal
                    if movement_vector[0] > 0:  # Left
                        press_key(Key.media_previous)
                    elif movement_vector[0] < 0:  # Right
                        press_key(Key.media_next)
            if scroll_lock.locked():
                scroll_lock.release()
            start_loc = None

def on_scroll(x, y, dx, dy):
    if thumb_lock.locked():
        if not scroll_lock.locked():
            scroll_lock.acquire()
        if dy > 0:
            press_key(Key.media_volume_up)
        elif dy < 0:
            press_key(Key.media_volume_down)


with MouseListener(on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
