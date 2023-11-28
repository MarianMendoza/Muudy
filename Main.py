import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import QFile, QTextStream, Qt



class MuudyWindow(QWidget):
    '''
    This is the main window, this window is used to open the Muudy application.

    This allows us to navigate between Activity Tracker and Personality Quiz.


    '''
    def __init__(self):
        '''
        Initialize the Muudy Windows.

        Creates and instance of the activity tracker and personality quiz, aswell as admin features.
        
        '''
        super().__init__()


        from activityTracker import ActivityTracker

        self.activity_tracker = ActivityTracker(self)  

        from personalityQuiz import PersonalityQuiz
        social_questions = ["Going out for food/drinks with friends", "Meeting up with somebody you know and going for a walk", "Being invited to a party", "Playing video games or watching a movie one-on-one with somebody", "Being kept up to date with the latest gossip"]
        hobby_questions = ["Engaging in a physical activity or sport for recreation", "Creating art, whether it's painting, drawing, or any other form", "Attending a live performance or event related to a personal interest", "Spending a quiet day immersed in a favorite book or series", "Exploring a new hobby or activity for the first time"]
        selfcare_questions = ["Reflecting on my achievements, no matter how small", "Engaging in a regular exercise routine to contribute to your well-being", "Getting a good night's sleep", "Engaging in some form of meditation", "Sitting at home and watching a movie with a pint of ice-cream"]
        organization_questions = ["Setting and achieving organizational goals", "Keeping your living or workspace neat and organized", "Collaborating with others in an organized manner", "Cleaning up the entire house to declutter the mind", "Having a systematic approach to managing responsibilities"]

        self.personality_quiz = PersonalityQuiz(social_questions,hobby_questions,selfcare_questions,organization_questions,self) #Create an instance of Activity Tracker

        self.init_ui()

    def init_ui(self):
        '''
        Sets up buttons
        
        '''
        self.setWindowTitle('Muudy Window')
        self.setGeometry(100, 100, 700, 300)


        self.main_label = QLabel('Muudy')
        self.main_label.setObjectName('mainLabel')

        self.admin_button = QPushButton('Admin')
        self.admin_button.setObjectName('adminButton')
        self.admin_button.clicked.connect(self.show_admin_feature)

        self.member_button = QPushButton('Member')
        self.member_button.setObjectName('memberButton')
        self.member_button.clicked.connect(self.show_personality_quiz)


        self.guests_button = QPushButton('Guests')
        self.guests_button.setObjectName('guestsButton')
        self.guests_button.clicked.connect(self.show_activity_tracker)

        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.admin_button)
        self.buttons_layout.addWidget(self.member_button)
        self.buttons_layout.addWidget(self.guests_button)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.main_label)  # Index 0
        self.stacked_widget.addWidget(self.activity_tracker)  # Index 1
        self.stacked_widget.addWidget(self.personality_quiz)  # Index 2


        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addLayout(self.buttons_layout)

        style_file = QFile('templates/styles.css')
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(style_file)
            self.setStyleSheet(stream.readAll())
            style_file.close()

    def show_activity_tracker(self):
        '''
        Switch to activity tracker
        
        '''
        self.admin_button.hide()
        self.member_button.hide()
        self.guests_button.hide()
        self.stacked_widget.setCurrentIndex(1)

    def show_personality_quiz(self):

        '''
        Switch the personality quiz
        
        '''
        self.admin_button.hide()
        self.member_button.hide()
        self.guests_button.hide()
        self.stacked_widget.setCurrentIndex(2)

    def show_admin_feature(self):

        '''
        Show admin Feature
        
        '''
        self.setWindowTitle('Admin')
        self.admin_popup = QWidget()
        self.admin_popup.setGeometry(700, 100, 300, 200)
        admin_layout = QVBoxLayout(self.admin_popup)
        admin_label = QLabel("Admin Feature not available.")
        admin_layout.addWidget(admin_label)
        self.admin_popup.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    muudy_window = MuudyWindow()
    muudy_window.show()

    sys.exit(app.exec())