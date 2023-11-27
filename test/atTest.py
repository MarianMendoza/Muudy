import pytest
from PyQt6.QtWidgets import QApplication
from activityTracker import ActivityTracker

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
    # Create an instance of ActivityTracker
    activity_tracker = ActivityTracker()

    # Simulate the user selecting the 'Happy' mood
    activity_tracker.mood_radio_buttons[0].setChecked(True)

    # Call the get_selected_mood method
    activity_tracker.get_selected_mood()

    # Check if the mood attribute is set correctly
    assert activity_tracker.mood == 'Happy'

    # Check if the stacked widget index is changed
    assert activity_tracker.stacked_widget.currentIndex() == 1


