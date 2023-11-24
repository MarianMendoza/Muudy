'''
Amy Marie Craven

'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QPushButton, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt,QFile, QTextStream
from PyQt6.QtGui import QFont

class PersonalityQuiz(QWidget):
    
    def __init__(self):
        super().__init__()

        
        self.init1()
    
    def init1(self):
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

        self.social_questions = ["Going out for food/drinks with friends", "Meeting up with somebody you know and going for a walk", "Being invited to a party", "Playing video games or watching a movie one-on-one with somebody", "Being kept up to date with the latest gossip"]
        self.hobby_questions = ["Engaging in a physical activity or sport for recreation", "Creating art, whether it's painting, drawing, or any other form", "Attending a live performance or event related to a personal interest", "Spending a quiet day immersed in a favorite book or series", "Exploring a new hobby or activity for the first time"]
        self.selfcare_questions = ["Reflecting on my achievements, no matter how small", "Engaging in a regular exercise routine to contribute to your well-being", "Getting a good night's sleep", "Engaging in some form of meditation", "Sitting at home and watching a movie with a pint of ice-cream"]
        self.organization_questions = ["Setting and achieving organizational goals", "Keeping your living or workspace neat and organized", "Collaborating with others in an organized manner", "Cleaning up the entire house to declutter the mind", "Having a systematic approach to managing responsibilities"]

        self.stacked_widget1 = QStackedWidget(self)
        self.categories = ['Social', 'Hobbies', 'Self-care', 'Organization']
        question_lists = [self.social_questions, self.hobby_questions, self.selfcare_questions, self.organization_questions]




        for category, questions in zip(self.categories, question_lists):
            page_widget = QWidget(self)
            page_layout = QVBoxLayout(page_widget)

            page_layout.addWidget(QLabel(f'{category} Category'))
            for i, question in enumerate(questions, 1):
                slider_label = QLabel(f'{i}: {question}')
                slider = QSlider(Qt.Orientation.Horizontal)  # Horizontal orientation
                slider.setMinimum(1)  # Set the minimum value to 1
                slider.setMaximum(10)
                slider.setValue(1)  # Set the default value to 1

                page_layout.addWidget(slider_label)
                page_layout.addWidget(slider)

            self.stacked_widget1.addWidget(page_widget)

        self.stacked_widget1.setCurrentIndex(0)

        self.result_label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget1)

        self.personality_label = QLabel()
        layout.addWidget(self.personality_label)

        self.next_button = QPushButton('Next')
        if self.stacked_widget1.currentIndex() == 0:
            self.next_button.setVisible(False)
        self.next_button.clicked.connect(self.next_category)

        self.results_page = QWidget(self)
        results_layout = QVBoxLayout(self.results_page)
        results_layout.addWidget(self.result_label)
        results_layout.addWidget(self.next_button)

        self.setLayout(layout)
        self.setFixedSize(600, 400)

        self.setGeometry(100, 100, 700, 300)
        self.setWindowTitle('Personality Quiz')
        self.show()

    def show_admin_message(self):
        QMessageBox.information(self, "Admin Access", "Admin features are not implemented yet.")

    def start_questionnaire(self):
        self.stacked_widget1.setCurrentIndex(1)  # Start with the first category (index 1)
        self.next_button.setVisible(True)  # Show the "Next" button on the category questions pages
        self.layout().addWidget(self.next_button)

    def next_category(self):
        if self.current_page_index < len(self.categories) - 1:
            self.current_page_index += 1
            self.stacked_widget1.setCurrentIndex(self.current_page_index + 1)  # Adjust for the welcome page
        else:
            self.stacked_widget1.setCurrentIndex(len(self.categories) + 1)  # Adjust for the welcome page
            self.show_results()

    def show_results(self):
        for i in range(self.stacked_widget1.count()):
            page = self.stacked_widget1.widget(i)
            for j in range(page.layout().count()):
                item = page.layout().itemAt(j)
                if isinstance(item.widget(), QSlider):
                    self.happiness_values.append(item.widget().value())

        if all(score == 1 for score in self.happiness_values):
            self.result_label.setText("This site may not be for you. You don't seem to fit into any of our categories.\nIf you'd like to carry on to our activity tracker, feel free, but it may be inaccurate.")
            personality_type = ""
            self.stacked_widget1.addWidget(self.results_page)
            self.stacked_widget1.setCurrentWidget(self.results_page)
            return
    

        # Check if all prompts are at the highest value
        if all(score == 10 for score in self.happiness_values):
            self.result_label.setText("You have a consistently positive and enthusiastic approach to all aspects of life! "
                                    "You find maximum happiness in every category. \n If you'd like to be more specific \nfeel free to take the test again...")
            personality_type = 'Optimist'
        else:
            category_scores = {}
            max_question_scores = {}

            for i, category in enumerate(self.categories):
                category_scores[category] = sum(self.happiness_values[i * 5: (i + 1) * 5])
                max_question_scores[category] = max(self.happiness_values[i * 5: (i + 1) * 5])

            max_category = max(category_scores, key=lambda k: (category_scores[k], max_question_scores[k]))
            personality_type = self.personality_types[max_category]

            # Check if there are two categories with the same scores and the same max question scores
            equal_categories = [self.personality_types[cat] for cat, score in category_scores.items() if score == category_scores[max_category] and max_question_scores[cat] == max_question_scores[max_category]]

            if len(equal_categories) == 2:
                personality_type = f'{equal_categories[0]} and {equal_categories[1]}'
                descriptions = [self.descriptions[personality_type] for personality_type in equal_categories]
                description = f'You are a {personality_type}!\n\nDescriptions:\n\n1. {descriptions[0]}\n\n2. {descriptions[1]} \n\n Feel free to identify with whichever you prefer! You deserve it'
            else:
                description = f'You are a {personality_type}! \n {self.descriptions[personality_type]}'

            self.result_label.setText(description)

        self.stacked_widget1.addWidget(self.results_page)
        self.stacked_widget1.setCurrentWidget(self.results_page)

    def reset_questionnaire(self):
        self.stacked_widget1.setCurrentIndex(1)  # Go back to the first question page
        self.happiness_values = []  # Reset happiness values
        self.next_button.setVisible(True)  # Show the "Next" button on the category questions pages
        self.layout().addWidget(self.next_button)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    personalityTracker = PersonalityQuiz()
    personalityTracker.show()

    sys.exit(app.exec())