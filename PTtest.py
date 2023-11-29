import sys
from PyQt6.QtWidgets import QApplication,QSlider
from personalityQuiz import PersonalityQuiz  
from Main import MuudyWindow
import unittest

def test_category_with_highest_points_displays_correct_result():
    # Create the QApplication instance
    app = QApplication(sys.argv)
    mw = MuudyWindow()
    # Create an instance of PersonalityQuiz (replace the question lists with actual data)
    quiz = PersonalityQuiz([], [], [], [], mw)

    # Simulate answering questions and calculating points (replace with your actual logic)
    quiz.happiness_values = [10,10,10,10,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    # Simulate calling the show_results method
    quiz.show_results()

    # Print the actual result label text for debugging
    actual_result_label_text = quiz.result_label.text()
    print(f"Actual Result Label Text: {actual_result_label_text}")

    # Check if the result label contains the correct personality type based on the highest points
    expected_personality_type = "You are a Diplomat!"  # Replace with the expected personality type
    assert expected_personality_type.lower() in actual_result_label_text.lower(), f"Expected: {expected_personality_type}, Actual: {actual_result_label_text}"

    # Clean up
    app.quit()


class TestSliderValidity(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.quiz = PersonalityQuiz([], [], [], [], None)  # Pass appropriate question lists and muudy_window object

    def test_slider_validity(self):
        for i in range(self.quiz.stacked_widget.count()):
            page = self.quiz.stacked_widget.widget(i)
            for j in range(page.layout().count()):
                item = page.layout().itemAt(j)
                if isinstance(item.widget(), QSlider):
                    slider_value = item.widget().value()
                    self.assertTrue(1 <= slider_value <= 10, f"Slider value {slider_value} is not valid.")

    def tearDown(self):
        del self.quiz
        self.app.quit()

if __name__ == '__main__':
    unittest.main()


