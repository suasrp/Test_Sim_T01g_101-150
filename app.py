import streamlit as st
import json
import time

def load_questions(filename):
    """Load questions from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

class QuizApp:
    def __init__(self):
        # Load questions
        self.questions = load_questions('questions_20240928_101-150.json')
        self.current_question = 0
        self.score = 0
        self.start_time = time.time()
        self.time_limit = 60  # Time limit for the quiz in seconds

    def next_question(self):
        """Load and display the next question."""
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.display_question(question_data)
            self.current_question += 1
        else:
            self.end_quiz()

    def display_question(self, question_data):
        """Display the current question and options."""
        st.write(f"### Question {question_data['question_number']}")
        st.write(question_data["question"])

        if question_data["type"] == "multiple-choice":
            self.show_multiple_choice(question_data)
        elif question_data["type"] == "fill-in-the-blank":
            self.show_fill_in_the_blank()

        if st.button("Submit"):
            self.submit_answer(question_data)

    def show_multiple_choice(self, question_data):
        """Show multiple choice options."""
        options = st.multiselect("Select your answer(s):", question_data["options"], default=[])
        if 'answers' in question_data:  # Handle multiple correct answers
            self.selected_options = options
        else:  # Handle single correct answer
            self.selected_option = options[0] if options else None

    def show_fill_in_the_blank(self):
        """Show text entry for fill-in-the-blank questions."""
        self.answer_text = st.text_input("Your answer:")

    def submit_answer(self, question_data):
        """Evaluate the answer and proceed to the next question."""
        if question_data["type"] == "multiple-choice":
            self.handle_multiple_choice(question_data)
        elif question_data["type"] == "fill-in-the-blank":
            self.handle_fill_in_the_blank(question_data)
        self.next_question()

    def handle_multiple_choice(self, question_data):
        """Handle answer submission for multiple choice questions."""
        if 'answers' in question_data:
            selected_set = set(self.selected_options)
            correct_set = set(question_data["answers"])
            if selected_set == correct_set:
                self.score += 1
        else:
            if self.selected_option and self.selected_option == question_data["answer"]:
                self.score += 1

    def handle_fill_in_the_blank(self, question_data):
        """Handle answer submission for fill-in-the-blank questions."""
        if self.answer_text.strip() == question_data["answer"]:
            self.score += 1

    def end_quiz(self):
        """Display the final score."""
        elapsed_time = int(time.time() - self.start_time)
        if elapsed_time > self.time_limit:
            st.write(f"⏳ Time's up! Your final score is {self.score}/{len(self.questions)}.")
        else:
            st.write(f"🎉 Your final score is {self.score}/{len(self.questions)}.")
        st.stop()

def main():
    st.title("Quiz Application")
    quiz_app = QuizApp()
    quiz_app.next_question()

if __name__ == "__main__":
    main()
