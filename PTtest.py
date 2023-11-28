import sys
from PyQt6.QtWidgets import QApplication
from personalityQuiz import PersonalityQuiz  
from Main import MuudyWindow

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

