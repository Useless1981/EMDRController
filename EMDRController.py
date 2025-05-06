import sys
from typing import List

from XInput import get_events, set_vibration, EVENT_BUTTON_PRESSED, Event
from time import time


class EMDRController:

    def __init__(self):
        self.vibration:bool = False
        self.interval_in_sec:float = 1.0
        self.strength:float = 0.5
        self.controller_0: int = 0
        self.controller_1: int = 1
        self.activ:int = self.controller_0
        self.idle:int = self.controller_1
        self.starting_time: float = time()
        self.max_interval: float = 3.0
        self.min_interval: float = 0.5
        self.interval_steps: float = 0.2
        self.max_strength:float = 1.0
        self.min_strength:float = 0.1
        self.strength_steps: float = 0.1
        self.starting_messages: List[str] = ['EMDR Controller started.\n',
                                            'Press X to start the vibration.',
                                            'Press A to stop the vibration.',
                                            'Press DPad Up to increase the vibration.',
                                            'Press DPad Down to decrease the vibration.',
                                            'Press DPad Left to decrease the vibration interval.',
                                            'Press DPad Up to increase the vibration interval.',
                                            'Press Start to quit.']

    # Main Loop
    def start(self) -> None:
        for message in self.starting_messages: print(message)
        while True:
            if time() > (self.starting_time + self.interval_in_sec):
                self.starting_time = time()
                self.switch_vibration()
                self.vibrate()
            events = get_events()
            self.handle_events(events)

    # Handles Button Events
    def handle_events(self, events: List[Event]) -> None:
        for event in events:
            if event.type == EVENT_BUTTON_PRESSED:
                if event.button == "X":
                    self.vibration = True
                    self.vibrate()
                    print('Starting Vibration ...')
                elif event.button == "A":
                    self.vibration = False
                    self.vibrate()
                    print('Stopping Vibration ...')
                elif event.button == "START":
                    print('Shutting Down ...')
                    self.stop()
                elif event.button == "DPAD_UP":
                    self.increase_strength()
                    percentage = int(round(self.strength * 100, 0))
                    print('Strength now at ' + str(percentage) + ' %')
                elif event.button == "DPAD_DOWN":
                    self.decrease_strength()
                    percentage = int(round(self.strength * 100, 0))
                    print('Strength now at ' + str(percentage) + ' %')
                elif event.button == "DPAD_LEFT":
                    self. decrease_interval()
                    print('Interval now at ' + str(self.interval_in_sec) + ' Seconds')
                elif event.button == "DPAD_RIGHT":
                    self.increase_interval()
                    print('Interval now at ' + str(self.interval_in_sec) + ' Seconds')


    # Decreases the time interval between switches (Unit Test)
    def decrease_interval(self) -> None:
        self.interval_in_sec -= self.interval_steps
        if self.interval_in_sec < self.min_interval:
            self.interval_in_sec = self.min_interval

    # Increases the time interval between switches (Unit Test)
    def increase_interval(self) -> None:
        self.interval_in_sec += self.interval_steps
        if self.interval_in_sec > self.max_interval:
            self.interval_in_sec = self.max_interval

    # Increases the vibration strength (Unit Test)
    def increase_strength(self) -> None:
        self.strength += self.strength_steps
        if self.strength > self.max_strength:
            self.strength = self.max_strength

    # Decreases the vibration strength (Unit Test)
    def decrease_strength(self) ->None:
        self.strength -= self.strength_steps
        if self.strength < self.min_strength:
            self.strength = self.min_strength

    # Stops the Program
    def stop(self) -> None:
        sys.exit(0)

    # Switches the vibration from one to the other game controller (Unit Test)
    def switch_vibration(self) -> None:
        if self.activ == self.controller_0:
            self.activ = self.controller_1
            self.idle = self.controller_0
        else:
            self.activ = self.controller_0
            self.idle = self.controller_1

    # Controls the vibration of the game controllers. self.vibration toggles this on and off.
    def vibrate(self) -> None:
        if self.vibration:
            set_vibration(self.idle, 0, 0)
            set_vibration(self.activ, self.strength, self.strength)
        else:
            set_vibration(self.idle, 0, 0)
            set_vibration(self.activ, 0, 0)


