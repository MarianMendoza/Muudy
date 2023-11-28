import pytest
from PyQt6.QtWidgets import QApplication
from unittest.mock import MagicMock  # Import MagicMock for creating a mock object
from a import ActivityTracker
 
@pytest.fixture
def app():
    """
    Fixture to create a QApplication instance before each test.
    """
    application = QApplication([])
    yield application
    application.quit()

def test_get_selected_mood(app):
    """
    Test the get_selected_mood method of ActivityTracker.
    """
    # Create a mock muudy_window
    muudy_window_mock = MagicMock()

    # Create an instance of ActivityTracker with the mock muudy_window
    activity_tracker = ActivityTracker(muudy_window_mock)

    # Simulate the user selecting the 'Happy' mood
    activity_tracker.mood_radio_buttons[0].setChecked(True)

    # Call the get_selected_mood method
    activity_tracker.get_selected_mood()

    # Check if the mood attribute is set correctly
    assert activity_tracker.mood == 'Happy'

    # Check if the stacked widget index is changed
    assert activity_tracker.stacked_widget.currentIndex() == 1
