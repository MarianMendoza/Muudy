import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QRadioButton, QFormLayout, QDialog, QWidgetItem, QLayoutItem


class MoodSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Select Your Mood')
        self.setGeometry(600, 400, 600, 400)

        self.mood_layout = QFormLayout()

        self.mood_radio_buttons = [
            QRadioButton('Happy'),
            QRadioButton('Sad'),
            QRadioButton('Neutral')
        ]

        for button in self.mood_radio_buttons:
            self.mood_layout.addWidget(button)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)

        self.mood_layout.addWidget(self.ok_button)
        self.setLayout(self.mood_layout)

    def get_selected_mood(self):
        for button in self.mood_radio_buttons:
            if button.isChecked():
                return button.text()
        return None


class ActivityTracker(QWidget):
    def __init__(self, initial_mood):
        super().__init__()

        self.selected_activities = set()
        self.mood = initial_mood

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Activity Tracker')
        self.setGeometry(600, 400, 600, 400)

        # Create main layout
        self.main_layout = QVBoxLayout()

        # Points
        self.social_points = 0
        self.hobbies_points = 0
        self.organizational_points = 0
        self.self_care_points = 0
        # These points are appended in the following order. So max/min point is picked then returns output.
        self.point_dict = {"Social": 0, "Hobbies": 0, "Organizational": 0, "Self-Care": 0}

        # Create category group boxes
        self.social_group_box = self.create_category_group_box('Social', ['Drinking', 'Cafe Hopping', 'People Watching'])
        self.hobbies_group_box = self.create_category_group_box('Hobbies', ['Draw', 'Watch Movies', 'Read'])
        self.organizational_group_box = self.create_category_group_box('Organizational', ['Study', 'Read Articles', 'Budget'])
        self.self_care_group_box = self.create_category_group_box('Self-care', ['Meditate', 'Yoga', 'Tidy Safe Space'])

        # Create button to display selected activities
        show_activities_button = QPushButton('Select Activities')
        show_activities_button.clicked.connect(self.show_results_no_personality)

        # Add components to main layout
        self.main_layout.addWidget(self.social_group_box)
        self.main_layout.addWidget(self.hobbies_group_box)
        self.main_layout.addWidget(self.organizational_group_box)
        self.main_layout.addWidget(self.self_care_group_box)

        self.main_layout.addWidget(show_activities_button)

        # Set main layout
        self.setLayout(self.main_layout)

    def create_category_group_box(self, category, activities):
        group_box = QGroupBox(category)
        layout = QVBoxLayout()

        # Create check boxes for each activity
        for activity in activities:
            check_box = QCheckBox(activity)
            check_box.clicked.connect(self.activity_selected)
            layout.addWidget(check_box)

        group_box.setLayout(layout)

        return group_box

    def activity_selected(self):
        sender = self.sender()
        activity = sender.text()

        if sender.isChecked():
            self.selected_activities.add(activity)

            # Check the category and increment points accordingly
            if activity in ['Drinking', 'Cafe Hopping', 'People Watching']:
                self.social_points += 1
                self.point_dict["Social"] = self.social_points

            elif activity in ['Draw', 'Watch Movies', 'Read']:
                self.hobbies_points += 1
                self.point_dict["Hobbies"] = self.hobbies_points

            elif activity in ['Study', 'Read Articles', 'Budget']:
                self.organizational_points += 1
                self.point_dict["Organizational"] = self.organizational_points

            elif activity in ['Meditate', 'Yoga', 'Tidy Safe Space']:
                self.self_care_points += 1
                self.point_dict["Self-Care"] = self.self_care_points

        else:
            self.selected_activities.discard(activity)

    def show_results_no_personality(self):
        # Clear existing content
        self.clear_layout(self.main_layout)

        # Create new category group boxes based on selected activities
        self.no_personality_result_label = QLabel(f'Your mood is {self.mood}.\nThese are your results.')
        self.main_layout.addWidget(self.no_personality_result_label)

        self.no_personality_result_from_max = {
            "Social": "You Might be a diplomat!",
            "Hobbies": "You might be an explorer!",
            "Organizational": "You might be a sentinel!",
            "Self-Care": "You might be an analyst!"
        }

        # Find the key with the maximum value in the dictionary
        self.max_key = max(self.point_dict, key=self.point_dict.get)
        self.result_np = self.no_personality_result_from_max[self.max_key]

        # Display the result
        self.max_points_result_label = QLabel(self.result_np)
        self.main_layout.addWidget(self.max_points_result_label)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                item.widget().close()
            elif isinstance(item, QLayoutItem):
                self.clear_layout(item.layout())

            # Remove the item from layout
            layout.removeItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Ask for mood first, 
    mood_dialog = MoodSelectionDialog()
    # Here we made it so that if my mood_dialog is executed to get selected mood.
    if mood_dialog.exec() == True:
        selected_mood = mood_dialog.get_selected_mood()

        #Change window here.
        # Open ActivityTracker window with the selected mood
        tracker = ActivityTracker(selected_mood)
        tracker.show()

        sys.exit(app.exec())
