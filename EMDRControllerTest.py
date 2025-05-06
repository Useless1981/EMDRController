import unittest
from EMDRController import EMDRController
from XInput import Event, EVENT_BUTTON_PRESSED


class EMDRControllerTestcase(unittest.TestCase):

    def test_handle_events_X_pressed(self):
        controller = EMDRController()
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'X'
        event.button_id = 0x4000
        self.assertFalse(controller.vibration)
        controller.handle_events([event])
        self.assertTrue(controller.vibration)

    def test_handle_events_A_pressed(self):
        controller = EMDRController()
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'X'
        event.button_id = 0x4000
        self.assertFalse(controller.vibration)
        controller.handle_events([event])
        self.assertTrue(controller.vibration)
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'A'
        event.button_id = 0x1000
        controller.handle_events([event])
        self.assertFalse(controller.vibration)

    def test_handle_events_START_pressed(self):
        controller = EMDRController()
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'Start'
        event.button_id = 0x0010
        controller.handle_events([event])
        self.assertRaises(SystemExit)

    def test_handle_events_DPAD_UP_pressed(self):
        controller = EMDRController()
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'DPAD_UP'
        event.button_id = 0x0001
        strength = controller.strength
        controller.handle_events([event])
        self.assertGreater(controller.strength, strength)

    def test_handle_events_DPAD_DOWN_pressed(self):
        controller = EMDRController()
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'DPAD_DOWN'
        event.button_id = 0x0002
        strength = controller.strength
        controller.handle_events([event])
        self.assertLess(controller.strength, strength)

    def test_handle_events_DPAD_LEFT_pressed(self):
        controller = EMDRController()
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'DPAD_LEFT'
        event.button_id = 0x0004
        interval = controller.interval_in_sec
        controller.handle_events([event])
        self.assertLess(controller.interval_in_sec, interval)

    def test_handle_events_DPAD_RIGHT_pressed(self):
        controller = EMDRController()
        event = Event(0, EVENT_BUTTON_PRESSED)
        event.button = 'DPAD_RIGHT'
        event.button_id = 0x0008
        interval = controller.interval_in_sec
        controller.handle_events([event])
        self.assertGreater(controller.interval_in_sec, interval)

    def test_switch_vibration(self):
        controller = EMDRController()
        idle_controller = controller.idle
        active_controller = controller.activ
        controller.switch_vibration()
        self.assertEqual(idle_controller, controller.activ)
        self.assertEqual(active_controller, controller.idle)

    def test_increase_strength(self):
        controller = EMDRController()
        strength = controller.strength
        controller.increase_strength()
        self.assertGreater(controller.strength, strength)
        self.assertEqual(controller.strength, strength + controller.strength_steps)
        for times_to_run in range(1,50):
            controller.increase_strength()
        self.assertEqual(controller.max_strength, controller.strength)

    def test_decrease_strength(self):
        controller = EMDRController()
        strength = controller.strength
        controller.decrease_strength()
        self.assertLess(controller.strength, strength)
        self.assertEqual(controller.strength, strength - controller.strength_steps)
        for times_to_run in range(1,50):
            controller.decrease_strength()
        self.assertEqual(controller.min_strength, controller.strength)

    def test_decrease_interval(self):
        controller = EMDRController()
        interval = controller.interval_in_sec
        controller.decrease_interval()
        self.assertLess(controller.interval_in_sec, interval)
        self.assertEqual(controller.interval_in_sec, interval - controller.interval_steps)
        for times_to_run in range(1, 50):
            controller.decrease_interval()
        self.assertEqual(controller.min_interval, controller.interval_in_sec)

    def test_increase_interval(self):
        controller = EMDRController()
        interval = controller.interval_in_sec
        controller.increase_interval()
        self.assertGreater(controller.interval_in_sec, interval)
        self.assertEqual(controller.interval_in_sec, interval + controller.interval_steps)
        for times_to_run in range(1, 50):
            controller.increase_interval()
        self.assertEqual(controller.max_interval, controller.interval_in_sec)

if __name__ == '__main__':
    unittest.main()
