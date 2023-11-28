import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QRadioButton, QFormLayout, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QFont
from Main import MuudyWindow

class ActivityTracker(QWidget):
    '''
    Activity tracker class represents the widget for tracking users activity.

    This class allow uses to select their mood, and activities that were done that day.

    Returns appropriate output.
    
    '''


    
    def __init__(self,muudy_window,from_personality = False):
        '''
        Initializes the activity window

        Muudy_window, is the main window instance
        
        '''
        super().__init__()
        self.from_personality = from_personality

        self.selected_activities = set()
        self.mood = None
        # self.mood = None

        self.personality = None
        # print("AT:",self.personality)

        self.muudy_window = muudy_window

        self.init_ui()

    def init_ui(self):
        '''
        Initializes the ui for the activity tracker.
        
        '''
        self.setWindowTitle('Activity Tracker')
        self.setGeometry(100, 100, 700, 300)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)


        self.go_back_button = QPushButton("Back")
        self.go_back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.go_back_button)
        self.go_back_button.hide()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(button_layout)

        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        button_layout.addWidget(home_button)

        self.stacked_widget = QStackedWidget()

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

        self.activity_widget = QWidget()
        self.activity_layout = QVBoxLayout(self.activity_widget)

        self.social_points = 0
        self.hobbies_points = 0
        self.organizational_points = 0
        self.self_care_points = 0
        self.point_dict = {"Social": 0, "Hobbies": 0, "Organizational": 0, "Self-Care": 0}

        self.social_group_box = self.create_category_group_box('Social', ['Drinking', 'Cafe Hopping', 'People Watching'])
        self.hobbies_group_box = self.create_category_group_box('Hobbies', ['Draw', 'Watch Movies', 'Read'])
        self.organizational_group_box = self.create_category_group_box('Organizational', ['Study', 'Read Articles', 'Budget'])
        self.self_care_group_box = self.create_category_group_box('Self-care', ['Meditate', 'Yoga', 'Tidy Safe Space'])

        show_activities_button = QPushButton('Select Activities')
        show_activities_button.clicked.connect(self.show_results)

        self.activity_layout.addWidget(self.social_group_box)
        self.activity_layout.addWidget(self.hobbies_group_box)
        self.activity_layout.addWidget(self.organizational_group_box)
        self.activity_layout.addWidget(self.self_care_group_box)

        self.activity_layout.addWidget(show_activities_button)

        self.stacked_widget.addWidget(self.activity_widget)  # Placeholder widget for the activity tracker layout
        self.stacked_widget.setCurrentIndex(0)  # Set the initial widget to mood selection

        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)

        # self.go_back_button = QPushButton("Back")
        if self.stacked_widget.currentIndex() == 0:
            self.go_back_button.setVisible(False)
        # self.go_back_button.clicked.connect(self.go_back)

        

        main_layout.addWidget(self.stacked_widget)

    def go_back_to_personality(self):
        self.muudy_window.stacked_widget.setCurrentIndex(1)

    def create_category_group_box(self, category, activities):
        """
        Create a group box for a category with checkboxes for each activity.

        Args:
            category (str): The category name.
            activities (list): List of activity names in the category.

        Returns:
            QGroupBox: The created group box.
        """

        group_box = QGroupBox(category)
        layout = QVBoxLayout()

        for activity in activities:
            check_box = QCheckBox(activity)
            check_box.clicked.connect(self.activity_selected)
            layout.addWidget(check_box)

        group_box.setLayout(layout)

        return group_box
    
    def go_back(self):
        '''
        Go back button
        
        '''
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)
        if self.stacked_widget.currentIndex() == 0:
            self.go_back_button.hide()

    def go_home(self):
        '''
        Go Home
        
        '''
        self.muudy_window.admin_button.show()
        self.muudy_window.member_button.show()
        self.muudy_window.guests_button.show()
        self.muudy_window.stacked_widget.setCurrentIndex(0)

    def activity_selected(self):
        '''
        Handle the selection/deselection of an activity tracker
        
        '''
        sender = self.sender()
        activity = sender.text()

        if sender.isChecked():
            self.selected_activities.add(activity)

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

    def show_results(self):
        '''
        Show the results.
        '''
        # print(self.personality)

        if self.personality == None:

            self.stacked_widget.addWidget(self.results_widget)
            self.stacked_widget.setCurrentWidget(self.results_widget)

            self.no_personality_result_label = QLabel(f'You have chosen, {self.mood}.\nBased on our Muudy predictions.')

            self.clear_layout(self.results_layout)

            if not self.selected_activities:
                self.no_personality_result_label.setText("You have not chosen any activities. Please choose some for analysis.")
                self.results_layout.addWidget(self.no_personality_result_label)
                return

            self.results_layout.addWidget(self.no_personality_result_label)

            self.no_personality_result_from_max = {
                "Social": "You Might be a Diplomat!\nDiplomats are empathetic mediators, driven by ideals and harmony. They excel in understanding emotions, fostering connections, and navigating conflicts with grace.",
                "Hobbies": "You might be an Explorer!\nExplorers are adventurous creators, embracing spontaneity and excitement. They live in the present, adapting to change effortlessly, and are resourceful problem solvers with a zest for new experiences.",
                "Organizational": "You might be an Analyst!\nAnalysts are analytical thinkers, valuing logic and innovation. Their precision and intellectual curiosity drive them to seek knowledge, solve complex problems, and push boundaries.",
                "Self-Care": "You might be a Sentinels!\nSentinels are practical organizers, prioritizing stability and order. They thrive on responsibility, reliability, and attention to detail, ensuring efficiency and a secure environment."
            }
            self.personalities = {"Social": "Diplomat", "Hobbies": "Explorer", "Organizational": "Analyst", "Self-Care": "Sentinel"}

            self.max_key = max(self.point_dict, key=self.point_dict.get)
            if all(value == self.point_dict[self.max_key] for value in self.point_dict.values()):
                self.no_personality_result_label.setText("You've done a lot! Consider taking the Muudy Personality test for a more detailed analysis.")
                # self.results_layout.addWidget(self.no_personality_result_label)

            if self.mood == "Sad":
                excluded_keys = [key for key in self.personalities.keys() if key != self.max_key]
                self.result_np = "You might be a " + ", ".join([self.personalities[key].split('!')[0] for key in excluded_keys])
                self.result_np += ". Take a Muudy personality test to delve deeper."
            elif self.mood == "Neutral":
                self.result_np = "Try taking the personality test for a further analysis."
            else:
                self.result_np = self.no_personality_result_from_max[self.max_key]

            self.max_points_result_label = QLabel(self.result_np)
            self.max_points_result_label.setWordWrap(True)  # Enable word wrap
            self.results_layout.addWidget(self.max_points_result_label)

        elif self.personality != None:
            self.stacked_widget.addWidget(self.results_widget)
            self.stacked_widget.setCurrentWidget(self.results_widget)
            if self.mood == "Sad":
            # Check if the person is a Diplomat
                if self.personality == "Diplomat":
                    self.result_np = "You are feeling exhausted today. Diplomats often invest a lot of emotional energy in understanding and mediating others' conflicts. Maybe focus more on your social life"
                # Check if the person is a Sentinel
                elif self.personality == "Sentinel":
                    self.result_np = "You feel overwhelmed today. Sentinels may feel stressed when faced with disruptions to their planned and organized routines. Maybe focus more on your organization"
                # Check if the person is an Analyst
                elif self.personality == "Analyst":
                    self.result_np = "You may be mentally drained today. Analysts tend to spend a lot of time thinking deeply and analyzing complex information. Maybe focus more on self care"
                # Check if the person is an Explorer
                elif self.personality == "Explorer":
                    self.result_np = "You might be feeling a bit scattered today. Explorers often enjoy spontaneity, but too much can lead to a sense of chaos. Maybe focus more on your hobbies"
                else:
                    print("Error")
                    pass

            elif self.mood == "Happy":
                if self.personality == "Diplomat":
                    self.result_np = "You feel joyful today! Diplomats are likely celebrating the positive connections and resolutions they've achieved. Keep up the good work and stay social!"
                # Check if the person is a Sentinel
                elif self.personality == "Sentinel":
                    self.result_np = "You feel content and satisfied today. Sentinels appreciate stability and order, and your organized approach may have contributed to your happiness.Keep up the good work and stay organized"
                # Check if the person is an Analyst
                elif self.personality == "Analyst":
                    self.result_np = "You are intellectually fulfilled today. Analysts find happiness in solving complex problems and gaining new knowledge. Keep up the good work and focus on self care"
                # Check if the person is an Explorer
                elif self.personality == "Explorer":
                    self.result_np = "You feel excited and fulfilled today. Explorers thrive on new experiences, and your adventurous spirit may be the source of your happiness. Keep up the good work and focus on your hobbies"
                else:
                    print("Error")
                    pass
            
            elif self.mood == "Neutral":
                if self.personality == "Diplomat":
                    self.result_np = "You are feeling calm and balanced today. Diplomats often maintain a sense of harmony and balance even in neutral situations."
                # Check if the person is a Sentinel
                elif self.personality == "Sentinel":
                    self.result_np = "You are in a state of calm today. Sentinels appreciate stability and order, and your organized approach may contribute to your sense of calm."
                # Check if the person is an Analyst
                elif self.personality == "Analyst":
                    self.result_np = "You are in a reflective state today. Analysts often enjoy contemplative moments to think deeply and analyze information."
                # Check if the person is an Explorer
                elif self.personality == "Explorer":
                    self.result_np = "You are in a state of openness today. Explorers thrive on new experiences, and your neutral mood may be a result of your adaptable and open-minded nature."
                else:
                    print("Error")

            self.points_result_label = QLabel(self.result_np)
            self.points_result_label.setWordWrap(True)  # Enable word wrap
            self.results_layout.addWidget(self.points_result_label)

            # self.results_layout.addWidget(self.max_points_result_label)
            # else:
            #     print("Other Else")
            #     pass

            
    def get_selected_mood(self):
        '''
        Get selected Mood
        
        '''

        for button in self.mood_radio_buttons:
            if button.isChecked():
                self.mood = button.text()

                # Switch to the activity tracker layout
                self.stacked_widget.setCurrentIndex(1)
                self.go_back_button.show()

                return

    def clear_layout(self, layout):
        '''
        Clear the layout

        Args:
            Layout to be cleared
        
        '''
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item.widget(), QLabel):
                item.widget().deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)

        # Apply the external stylesheet
    style_file = QFile('templates/styles.css')
    if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())
        style_file.close()

    muudy_window = MuudyWindow()
    # muudy_window.show()


    sys.exit(app.exec())
