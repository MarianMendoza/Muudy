import sys
import pytest
from PyQt6.QtWidgets import QApplication, QGroupBox, QCheckBox
from unittest.mock import MagicMock  # Import MagicMock for creating a mock object
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


def test_max_daily_activities():
    app = QApplication(sys.argv)
    activity_tracker = ActivityTracker(None)  # Pass appropriate muudy_window object or set it to None if not needed

    max_activities = 3

    # Iterate through the categories and check the number of activities
    for category_layout in activity_tracker.activity_layout.children():
        if isinstance(category_layout, QGroupBox):  # Assuming the categories are QGroupBox
            category_name = category_layout.title()

            # Count the number of activities in the category
            activities_count = sum(isinstance(widget, QCheckBox) for widget in category_layout.children())

            assert activities_count <= max_activities, f"Too many activities in the {category_name} category."

    app.quit()

if __name__ == '__main__':
    test_max_daily_activities()
