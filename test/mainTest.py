import sys
import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from Main import MuudyWindow 

class TestMuudyWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = MuudyWindow()

    def test_button_clicks(self):
        # Test the 'Member' button click
        member_button = self.window.member_button
        self.assertEqual(self.window.stacked_widget.currentIndex(), 0)  # Initial index
        QTest.mouseClick(member_button, Qt.MouseButton.LeftButton)
        self.assertEqual(self.window.stacked_widget.currentIndex(), 2)  # PersonalityQuiz index

        # Test the 'Guests' button click
        guests_button = self.window.guests_button
        QTest.mouseClick(guests_button, Qt.MouseButton.LeftButton)
        self.assertEqual(self.window.stacked_widget.currentIndex(), 1)  # ActivityTracker index

        # Test the 'Admin' button click
        admin_button = self.window.admin_button
        QTest.mouseClick(admin_button, Qt.MouseButton.LeftButton)
        # Assuming the admin feature shows a popup or switches to a new layout, check the expected behavior here

    def tearDown(self):
        self.app.quit()

if __name__ == '__main__':
    unittest.main()