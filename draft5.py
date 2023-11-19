import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QPushButton, QStackedWidget

class HappinessTracker(QWidget):
    def __init__(self, social_questions, hobby_questions, selfcare_questions, organization_questions):
        super().__init__()

        self.happiness_values = []
        self.current_page_index = 0
        self.personality_types = {
            'Social': 'Diplomat',
            'Hobbies': 'Explorer',
            'Self-care': 'Analyst',
            'Organization': 'Sentinel'
        }

        self.descriptions = {
            'Diplomat': "Diplomats are empathetic mediators, driven by ideals and harmony. They excel in understanding emotions, fostering connections, and navigating conflicts with grace.",
            'Explorer': "Explorers are adventurous creators, embracing spontaneity and excitement. They live in the present, adapting to change effortlessly, and are resourceful problem solvers with a zest for new experiences.",
            'Analyst': "Analysts are analytical thinkers, valuing logic and innovation. Their precision and intellectual curiosity drive them to seek knowledge, solve complex problems, and push boundaries.",
            'Sentinel': "Sentinels are practical organizers, prioritizing stability and order. They thrive on responsibility, reliability, and attention to detail, ensuring efficiency and a secure environment."
        }

        self.social_questions = social_questions
        self.hobby_questions = hobby_questions
        self.selfcare_questions = selfcare_questions
        self.organization_questions = organization_questions

        self.init_ui()

    def init_ui(self):
        self.welcome_page = QWidget(self)
        welcome_layout = QVBoxLayout(self.welcome_page)
        welcome_label = QLabel("Welcome to Muudy!")
        begin_button = QPushButton("Begin")
        begin_button.clicked.connect(self.start_questionnaire)

        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(begin_button)

        self.stacked_widget = QStackedWidget(self)
        self.categories = ['Social', 'Hobbies', 'Self-care', 'Organization']
        question_lists = [self.social_questions, self.hobby_questions, self.selfcare_questions, self.organization_questions]

        self.stacked_widget.addWidget(self.welcome_page)

        for category, questions in zip(self.categories, question_lists):
            
            page_widget = QWidget(self)
            page_layout = QVBoxLayout(page_widget)

            if category == 'Social':
                page_widget.setStyleSheet('background-color: yellow;')
            elif category == "Hobbies":
                page_widget.setStyleSheet('background-color: pink;')
            elif category == "Self-care":
                page_widget.setStyleSheet('background-color: lightblue;')
            elif category == "Organization":
                page_widget.setStyleSheet('background-color: lightgreen;')



            page_layout.addWidget(QLabel(f'{category} Category'))
            for i, question in enumerate(questions, 1):
                slider_label = QLabel(f'{i}: {question}')
                slider = QSlider()
                slider.setOrientation(1)  # Horizontal orientation
                slider.setMinimum(1)  # Set the minimum value to 1
                slider.setMaximum(10)
                slider.setValue(1)  # Set the default value to 1
                #slider.valueChanged.connect(self.update_slider_label)

                page_layout.addWidget(slider_label)
                page_layout.addWidget(slider)

            self.stacked_widget.addWidget(page_widget)

        self.stacked_widget.setCurrentIndex(0)

        self.result_label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)

        self.personality_label = QLabel()
        layout.addWidget(self.personality_label)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_category)

        self.results_page = QWidget(self)
        results_layout = QVBoxLayout(self.results_page)
        results_layout.addWidget(self.result_label)
        results_layout.addWidget(self.next_button)

        self.restart_button = QPushButton('Restart')
        self.restart_button.clicked.connect(self.restart_questionnaire)
        results_layout.addWidget(self.restart_button)

        self.setLayout(layout)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Happiness Tracker')
        self.show()

    def start_questionnaire(self):
        self.stacked_widget.setCurrentIndex(1)  # Start with the first category (index 1)
        self.layout().addWidget(self.next_button)

    def update_slider_label(self):
        sender = self.sender()
        category_index = self.stacked_widget.currentIndex()
        category = self.categories[category_index - 1]  # Adjust for the welcome page
        prompt_number = sender.parent().layout().indexOf(sender) - 1
        prompt_label = sender.parent().layout().itemAt(prompt_number).widget()
        prompt_label.setText(f'Prompt {prompt_number}: {category} - {sender.value()}')

    def next_category(self):
        if self.current_page_index < len(self.categories) - 1:
            self.current_page_index += 1
            self.stacked_widget.setCurrentIndex(self.current_page_index + 1)  # Adjust for the welcome page
        else:
            self.stacked_widget.setCurrentIndex(len(self.categories) + 1)  # Adjust for the welcome page
            self.show_results()

    def show_results(self):
        personality_type = None  # Initialize personality_type outside the conditions

        for i in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(i)
            for j in range(page.layout().count()):
                item = page.layout().itemAt(j)
                if isinstance(item.widget(), QSlider):
                    self.happiness_values.append(item.widget().value())

        # Check if all prompts are at the highest value
        if all(score == 10 for score in self.happiness_values):
            self.result_label.setText("You have a consistently positive and enthusiastic approach to all aspects of life! "
                                    "You find maximum happiness in every category. If you'd like to be more specific feel free to take the test again...")
            personality_type = 'Optimist'
        elif all(score == 1 for score in self.happiness_values):
            self.result_label.setText("You haven't set any preferences, please retake the test or reevaluate your life.")
        else:
            category_scores = {}
            max_question_scores = {}

            for i, category in enumerate(self.categories):
                category_scores[category] = sum(self.happiness_values[i * 5: (i + 1) * 5])
                max_question_scores[category] = max(self.happiness_values[i * 5: (i + 1) * 5])

            max_category = max(category_scores, key=lambda k: (category_scores[k], max_question_scores[k]))
            personality_type = self.personality_types[max_category]

        if personality_type:
            description = self.descriptions[personality_type]
            self.result_label.setText(f'You are a {personality_type}!\n\n{description}')

        self.stacked_widget.addWidget(self.results_page)
        self.stacked_widget.setCurrentWidget(self.results_page)

    def restart_questionnaire(self):
        self.stacked_widget.setCurrentIndex(0)
        self.happiness_values = []
        self.result_label.clear()
        self.personality_label.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    social_questions = ["Going out for food/drinks with friends", "Meeting up with somebody you know and going for a walk", "Being invited to a party", "Playing video games or watching a movie one-on-one with somebody", "Being kept up to date with the latest gossip"]
    hobby_questions = ["Engaging in a physical activity or sport for recreation", "Creating art, whether it's painting, drawing, or any other form", "Attending a live performance or event related to a personal interest", "Spending a quiet day immersed in a favorite book or series", "Exploring a new hobby or activity for the first time"]
    selfcare_questions = ["Reflecting on my achievements, no matter how small", "Engaging in a regular exercise routine to contribute to your well-being", "Getting a good night's sleep", "Engaging in some form of meditation", "Sitting at home and watching a movie with a pint of ice-cream"]
    organization_questions = ["Setting and achieving organizational goals", "Keeping your living or workspace neat and organized", "Collaborating with others in an organized manner", "Cleaning up the entire house to declutter the mind", "Having a systematic approach to managing responsibilities"]

    ex = HappinessTracker(social_questions, hobby_questions, selfcare_questions, organization_questions)
    sys.exit(app.exec_())
