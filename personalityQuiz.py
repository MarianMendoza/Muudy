import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QPushButton, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from Main import MuudyWindow
from activityTracker import ActivityTracker

class PersonalityQuiz(QWidget):
    
    def __init__(self, social_questions, hobby_questions, selfcare_questions, organization_questions,muudy_window):
        super().__init__()

        # Initialize attributes
        self.muudy_window = muudy_window
        self.happiness_values = []
        self.current_page_index = 0

        # Mapping of personality categories to types
        self.personality_types = {
            'Social': 'Diplomat',
            'Hobbies': 'Explorer',
            'Self-care': 'Analyst',
            'Organization': 'Sentinel'
        }

        # Initialize the activity tracker
        self.activity_tracker = ActivityTracker(muudy_window, from_personality=True)



        # Descriptions of different personality types
        self.descriptions = {
            'Diplomat': "Diplomats are empathetic mediators, driven by ideals and harmony. They excel in understanding emotions, fostering connections, and navigating conflicts with grace.",
            'Explorer': "Explorers are adventurous creators, embracing spontaneity and excitement. They live in the present, adapting to change effortlessly, and are resourceful problem solvers with a zest for new experiences.",
            'Analyst': "Analysts are analytical thinkers, valuing logic and innovation. Their precision and intellectual curiosity drive them to seek knowledge, solve complex problems, and push boundaries.",
            'Sentinel': "Sentinels are practical organizers, prioritizing stability and order. They thrive on responsibility, reliability, and attention to detail, ensuring efficiency and a secure environment."
        }

        # Set question attributes
        self.social_questions = social_questions
        self.hobby_questions = hobby_questions
        self.selfcare_questions = selfcare_questions
        self.organization_questions = organization_questions

        # Initialize the user interface
        self.init_ui()
    
    def init_ui(self):
        """
        Initializes the user interface for the Muudy's personality quiz application.
        """
        # Start Page
        self.start_page = QWidget(self)
        start_layout = QVBoxLayout(self.start_page)
        welcome_label = QLabel("Welcome to Muudy's personality quiz!\n"
                               "Please answer the following questions by providing how happy they make you\n"
                               "feel using the slider")

        begin_button = QPushButton("Begin Quiz")
        begin_button.clicked.connect(self.start_questionnaire)

        start_layout.addWidget(welcome_label)
        start_layout.addWidget(begin_button)

        # Stacked Widget for Categories
        self.stacked_widget = QStackedWidget(self)
        self.categories = ['Social', 'Hobbies', 'Self-care', 'Organization']
        question_lists = [self.social_questions, self.hobby_questions, self.selfcare_questions, self.organization_questions]

        self.stacked_widget.addWidget(self.start_page)

        for category, questions in zip(self.categories, question_lists):
            # Page for each category
            page_widget = QWidget(self)
            page_layout = QVBoxLayout(page_widget)

            page_layout.addWidget(QLabel(f'{category} Category'))

            # Add sliders for each question
            for i, question in enumerate(questions, 1):
                slider_label = QLabel(f'{i}: {question}')
                slider = QSlider(Qt.Orientation.Horizontal)  # Horizontal orientation
                slider.setMinimum(1)  # Set the minimum value to 1
                slider.setMaximum(10)
                slider.setValue(1)  # Set the default value to 1

                page_layout.addWidget(slider_label)
                page_layout.addWidget(slider)

            self.stacked_widget.addWidget(page_widget)

        self.stacked_widget.setCurrentIndex(0)

        # Result Page
        
        self.result_label = QLabel()
        layout = QVBoxLayout()

        layout.addLayout(self.create_button_layout())


        layout.addWidget(self.stacked_widget)


        self.personality_label = QLabel()
        layout.addWidget(self.personality_label)

        # Next Button
        self.next_button = QPushButton('Next')
        if self.stacked_widget.currentIndex() == 0:
            self.next_button.setVisible(False)
        self.next_button.clicked.connect(self.next_category)

        

        # Activity Tracker Button
        self.at_button = QPushButton('Go to Activity Tracker')
        self.at_button.setObjectName('atButton')
        self.at_button.clicked.connect(self.show_activity_tracker)
        self.stacked_widget.addWidget(self.at_button)

        self.stacked_widget.addWidget(self.activity_tracker)
        self.results_page = QWidget(self)
        results_layout = QVBoxLayout(self.results_page)
        results_layout.addWidget(self.result_label)
        results_layout.addWidget(self.next_button)
        results_layout.addWidget(self.at_button)
        self.at_button.hide()

        self.setLayout(layout)

        # Set window properties
        # self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Happiness Tracker')
        self.show()

    def start_questionnaire(self):
        """
        Starts the personality questionnaire by displaying the questions for the first category.
        """
        # Set the current index of the stacked widget to the first category
        self.stacked_widget.setCurrentIndex(1)
        
        # Show the "Next" button on the category questions pages
        self.next_button.setVisible(True)
        
        # Add the "Next" button to the layout
        self.layout().addWidget(self.next_button)

    
    
    def next_category(self):
        """
        Moves to the next category in the personality questionnaire or shows results if all categories are completed.
        """
        # Check if there are more categories to display
        if self.current_page_index < len(self.categories) - 1:
            # Move to the next category
            self.current_page_index += 1
            self.stacked_widget.setCurrentIndex(self.current_page_index + 1)  # Adjust for the welcome page
        else:
            # Show results if all categories are completed
            self.stacked_widget.setCurrentIndex(len(self.categories) + 1)  # Adjust for the welcome page
            self.show_results()

    def go_home(self):
        '''
        opening the home page
        '''
        self.muudy_window.admin_button.show()
        self.muudy_window.member_button.show()
        self.muudy_window.guests_button.show()
        self.muudy_window.stacked_widget.setCurrentIndex(0)

    def show_activity_tracker(self):
        """
        Switch to the Activity Tracker page within the PersonalityQuiz widget.

        This method hides the results page, hides the 'Next' button,
        sets the current index of the stacked widget to the Activity Tracker page,
        and applies the stylesheet for the Activity Tracker.
        """
        # Get the index of the Activity Tracker page in the stacked widget

        activity_tracker_index = self.stacked_widget.indexOf(self.activity_tracker)
        self.activity_tracker.personality = self.personality_type
        # print("PT:" , self.personality_type)

        # Hide the results page and 'Next' button
        self.results_page.hide()
        self.next_button.hide()
        self.home_button.hide()

        # Set the current index to the Activity Tracker page
        self.stacked_widget.setCurrentIndex(activity_tracker_index)

    def show_results(self):
        """
        Collects happiness values from the questionnaire and displays the personality quiz results.

        Returns:
        - None
        """
        # Collect happiness values from the questionnaire

        for i in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(i)
            for j in range(page.layout().count()):
                item = page.layout().itemAt(j)
                if isinstance(item.widget(), QSlider):
                    self.happiness_values.append(item.widget().value())

        # Check if all prompts have the lowest value
        if all(score == 1 for score in self.happiness_values):
            self.result_label.setText("This site may not be for you. You don't seem to fit into any of our categories.\n"
                                      "If you'd like to carry on to our activity tracker, feel free, but it may be inaccurate.")
            self.personality_type = ""
            self.stacked_widget.addWidget(self.results_page)
            self.stacked_widget.setCurrentWidget(self.results_page)
            return

        # Check if all prompts have the highest value
        if all(score == 10 for score in self.happiness_values):
            self.result_label.setText("You have a consistently positive and enthusiastic approach to all aspects of life! "
                                      "You find maximum happiness in every category. \n If you'd like to be more specific "
                                      "\nfeel free to take the test again...")
            self.personality_type = ''
        else:
            # Calculate scores for each category and identify the personality type
            category_scores = {}
            max_question_scores = {}

            for i, category in enumerate(self.categories):
                category_scores[category] = sum(self.happiness_values[i * 5: (i + 1) * 5])
                max_question_scores[category] = max(self.happiness_values[i * 5: (i + 1) * 5])

            max_category = max(category_scores, key=lambda k: (category_scores[k], max_question_scores[k]))
            self.personality_type = self.personality_types[max_category]

            # Check if there are two categories with the same scores and the same max question scores
            equal_categories = [self.personality_types[cat] for cat, score in category_scores.items() if
                                score == category_scores[max_category] and max_question_scores[cat] == max_question_scores[max_category]]

            if len(equal_categories) == 2:
                self.personality_type = f'{equal_categories[0]} and {equal_categories[1]}'
                descriptions = [self.descriptions[self.personality_type] for personality_type in equal_categories]
                description = f'You are a {self.personality_type}!\n\nDescriptions:\n\n1. {descriptions[0]}\n\n2. {descriptions[1]} \n\n Feel free to identify with whichever you prefer! You deserve it'

            else:
                description = f'You are a {self.personality_type}! \n {self.descriptions[self.personality_type]}'


            print(self.personality_type)

            self.result_label.setText(description)
            self.result_label.setWordWrap(True)

        # Show the results page and the Activity Tracker button
        self.stacked_widget.addWidget(self.results_page)
        self.stacked_widget.setCurrentWidget(self.results_page)
        self.at_button.show()
        self.next_button.hide()
    
    def create_button_layout(self):
        """
        Creates a horizontal layout for buttons, including a 'Home' button.

        Returns:
        - QHBoxLayout: The created horizontal button layout.
        """
        button_layout = QHBoxLayout()
        button_layout.addStretch(2)

        self.home_button = QPushButton('Home')
        self.home_button.setObjectName('homeButton')
        self.home_button.clicked.connect(self.go_home)
        button_layout.addWidget(self.home_button)

        return button_layout
    

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    # style_file = QFile('templates/styles.css')
    # if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
    #     stream = QTextStream(style_file)
    #     app.setStyleSheet(stream.readAll())
    #     style_file.close()

    muudy_window = MuudyWindow()
    muudy_window.show()


    sys.exit(app.exec())
