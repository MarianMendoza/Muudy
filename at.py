import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel


class ActivityTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_activities = set()  # Using a set to avoid duplicates

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Activity Tracker')
        self.setGeometry(600, 400,600,400)

        # Create main layout
        main_layout = QVBoxLayout()

        # Points
        self.social_points = 0
        self.hobbies_points = 0
        self.organizational_points = 0
        self.self_care_points = 0
        # These points are appended in the following order. So max/min point is picked then returns output.
        self.point_dict = {"Social": 0, "Hobbies":0, "Organizational":0, "Self-Care": 0}

        # Create category group boxes
        social_group_box = self.create_category_group_box('Social', ['Drinking', 'Cafe Hopping', 'People Watching'])
        hobbies_group_box = self.create_category_group_box('Hobbies', ['Draw', 'Watch Movies', 'Read'])
        organizational_group_box = self.create_category_group_box('Organizational', ['Study', 'Read Articles', 'Budget'])
        self_care_group_box = self.create_category_group_box('Self-care', ['Meditate', 'Yoga', 'Tidy Safe Space'])

        # Create button to display selected activities
        show_activities_button = QPushButton('Select Activities')
        show_activities_button.clicked.connect(self.show_selected_activities)

        # Create label to display selected activities
        self.activities_label = QLabel('Selected Activities: ')

        # Add components to main layout
        main_layout.addWidget(social_group_box)
        main_layout.addWidget(hobbies_group_box)
        main_layout.addWidget(organizational_group_box)
        main_layout.addWidget(self_care_group_box)

        main_layout.addWidget(show_activities_button)
        main_layout.addWidget(self.activities_label)

        # Set main layout
        self.setLayout(main_layout)

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

            # print(self.point_dict)
        else:
            self.selected_activities.discard(activity)

    def show_selected_activities(self):
        selected_activities_text = ', '.join(self.selected_activities)
        self.activities_label.setText(f'Selected Activities: {selected_activities_text}')
        self.select_max()

    def select_max(self):
        max_points = max(self.point_dict, key=self.point_dict.get)
        print("Max", max_points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tracker = ActivityTracker()
    tracker.show()
    sys.exit(app.exec())
