import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


class Test_Record_User_Activity(unittest.TestCase):
    def test_start_recording(self):
        pass

    def test_stop_and_save_recording(self):
        pass
