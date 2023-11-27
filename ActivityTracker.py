'''

Marian Angeles Mendoza



'''
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QRadioButton, QFormLayout, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QFont

class ActivityTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_activities = set()
        self.mood = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Activity Tracker')
        self.setGeometry(100, 100, 700, 300)

        # Add a button for switching to admin feature
        admin_button = QPushButton('Admin')
        admin_button.clicked.connect(self.show_admin_feature)
        admin_button.setObjectName("adminButton")


 
        # Create a horizontal layout for the admin button
        admin_layout = QHBoxLayout()
        admin_layout.addStretch(1)

        admin_layout.addWidget(admin_button)


        #Back Button
        go_back_button = QPushButton("Back")
        go_back_button.clicked.connect(self.go_back)
        admin_layout.addWidget(go_back_button)

        # Add the admin layout to the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(admin_layout)

        #Home
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        admin_layout.addWidget(home_button)

        # Create a stacked widget for different screens
        self.stacked_widget = QStackedWidget()

        # Mood selection layout
        mood_widget = QWidget()
        self.mood_layout = QFormLayout(mood_widget)
        self.mood_radio_buttons = [
            QRadioButton('Happy'),
            QRadioButton('Sad'),
            QRadioButton('Neutral')
        ]
        for button in self.mood_radio_buttons:
            self.mood_layout.addWidget(button)
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.get_selected_mood)
        self.mood_layout.addWidget(self.ok_button)
        self.stacked_widget.addWidget(mood_widget)

        # Activity tracker layout
        self.activity_widget = QWidget()
        self.activity_layout = QVBoxLayout(self.activity_widget)

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

        # Add components to the activity layout
        self.activity_layout.addWidget(self.social_group_box)
        self.activity_layout.addWidget(self.hobbies_group_box)
        self.activity_layout.addWidget(self.organizational_group_box)
        self.activity_layout.addWidget(self.self_care_group_box)

        self.activity_layout.addWidget(show_activities_button)

        # Add the activity layout to the stacked widget
        self.stacked_widget.addWidget(self.activity_widget)  # Placeholder widget for the activity tracker layout
        self.stacked_widget.setCurrentIndex(0)  # Set the initial widget to mood selection

        # Results layout
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)

        # Add the stacked widget to the main layout
        main_layout.addWidget(self.stacked_widget)

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
    
    def go_back(self):
        # Return to the last page

        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    def go_home(self):
        # Return to the last page
        self.stacked_widget.setCurrentIndex(2)


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
        self.stacked_widget.addWidget(self.results_widget)
        self.stacked_widget.setCurrentWidget(self.results_widget)

        self.no_personality_result_label = QLabel(f'You have chosen, {self.mood}.\nBased on our Muudy predictions.')

        # Clear existing content
        self.clear_layout(self.results_layout)

        # Check if no activities were selected
        if not self.selected_activities:
            self.no_personality_result_label.setText("You have not chosen any activities. Please choose some for analysis.")
            self.results_layout.addWidget(self.no_personality_result_label)
            return

        # Create new category group boxes based on selected activities
        self.results_layout.addWidget(self.no_personality_result_label)

        self.no_personality_result_from_max = {
            "Social": "You Might be a Diplomat!\nDiplomats are empathetic mediators, driven by ideals and harmony. They excel in understanding emotions, fostering connections, and navigating conflicts with grace.",
            "Hobbies": "You might be an Explorer!\nExplorers are adventurous creators, embracing spontaneity and excitement. They live in the present, adapting to change effortlessly, and are resourceful problem solvers with a zest for new experiences.",
            "Organizational": "You might be an Analyst!\nAnalysts are analytical thinkers, valuing logic and innovation. Their precision and intellectual curiosity drive them to seek knowledge, solve complex problems, and push boundaries.",
            "Self-Care": "You might be a Sentinels!\nSentinels are practical organizers, prioritizing stability and order. They thrive on responsibility, reliability, and attention to detail, ensuring efficiency and a secure environment."
        }
        self.personalities = {"Social": "Diplomat", "Hobbies": "Explorer", "Organizational": "Analyst", "Self-Care": "Sentinel"}

        # Find the key with the maximum value in the dictionary
        self.max_key = max(self.point_dict, key=self.point_dict.get)
        if all(value == self.point_dict[self.max_key] for value in self.point_dict.values()):
            self.no_personality_result_label.setText("You've done a lot! Consider taking the Muudy Personality test for a more detailed analysis.")
            # self.results_layout.addWidget(self.no_personality_result_label)

        # Check if mood is "Sad" and exclude the max key
        if self.mood == "Sad":
            excluded_keys = [key for key in self.personalities.keys() if key != self.max_key]
            self.result_np = "You might be a " + ", ".join([self.personalities[key].split('!')[0] for key in excluded_keys])
            self.result_np += ". Take a Muudy personality test to delve deeper."
        elif self.mood == "Neutral":
            self.result_np = "Try taking the personality test for a further analysis."
        else:
            # Display the result based on mood
            self.result_np = self.no_personality_result_from_max[self.max_key]

        # Display the result
        self.max_points_result_label = QLabel(self.result_np)
        self.max_points_result_label.setWordWrap(True)  # Enable word wrap
        self.results_layout.addWidget(self.max_points_result_label)

    def show_admin_feature(self):
        self.setWindowTitle('Admin')
        self.admin_popup = QWidget()
        self.admin_popup.setGeometry(700, 100, 300, 200)
        admin_layout = QVBoxLayout(self.admin_popup)
        admin_label = QLabel("Admin Feature not available.")
        admin_layout.addWidget(admin_label)
        self.admin_popup.show()

    def get_selected_mood(self):
        for button in self.mood_radio_buttons:
            if button.isChecked():
                self.mood = button.text()

                # Switch to the activity tracker layout
                self.stacked_widget.setCurrentIndex(1)
                return

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item.widget(), QLabel):
                item.widget().deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
        # Apply the external stylesheet
    style_file = QFile('styles.css')
    if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())
        style_file.close()


    tracker = ActivityTracker()
    tracker.show()

    sys.exit(app.exec())
