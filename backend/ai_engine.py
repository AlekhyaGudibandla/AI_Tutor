from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
import json
import re
import logging

# Configuring logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
GROQ_API_KEY = os.getenv("OPENAI_API_KEY")


def get_llm():
    try:
        return ChatGroq(
            temperature=0.7,
            model_name='llama-3.3-70b-versatile',
            groq_api_key=GROQ_API_KEY
        )
    except Exception as e:
        raise Exception(f"Failed to initialize Groq LLM: {str(e)}")


def generate_tutoring_response(subject, level, question, learning_style, background, language):
    """
    Generate a personalized tutoring response based on user preferences.
    """
    try:
        llm = get_llm()  # ✅ Assign the LLM instance

        prompt = _create_tutoring_prompt(subject, level, question, learning_style, background, language)

        logger.info(f"Generating tutoring response for subject: {subject}, level: {level}, language: {language}")
        response = llm([HumanMessage(content=prompt)])  # ✅ Now works

        return _format_tutoring_response(response.content, learning_style)

    except Exception as e:
        logger.error(f"Error generating tutoring response: {str(e)}")
        raise Exception(f"Failed to generate tutoring response: {str(e)}")



def _create_tutoring_prompt(subject, level, question, learning_style, background, language):
    """
    Helper function to create well-structured tutoring prompt
    """
    prompt = f"""
You are an expert tutor specializing in {subject} at a {level} level.

STUDENT PROFILE:
- Background Knowledge: {background}
- Learning Style preference: {learning_style}
- Preferred Language: {language}

QUESTION:
{question}

INSTRUCTIONS:
1. Provide a clear, educational explanation that directly addresses the question.
2. Tailor your explanation to a {background} student at {level} level.
3. Use {language} as your primary language.
4. Format your response with appropriate markdown for readability.

LEARNING STYLE ADAPTATIONS:
- For visual learners: Include descriptions of visual concepts, diagrams, or mental models.
- For text-based learners: Provide clear, structured explanation with defined concepts.
- For hands-on learners: Include practical examples, exercises, or applications.

Your explanation should be educational, accurate, and engaging, helping the student understand the topic deeply.
"""
    return prompt


def _format_tutoring_response(content, learning_style):
    """Helper function to format the tutoring response based on learning style"""

    if learning_style == "Visual":
        return content + "\n\n*Note: Visualize these concepts as you read for better retention.*"
    elif learning_style == "Hands-on":
        return content + "\n\n*Note: Try working through the examples yourself to reinforce your learning.*"
    else:
        return content


def _create_quiz_prompt(subject, level, num_questions):
    """
    Helper function to create well-structured quiz generation prompt with hints
    """
    return f"""
    Create a {level} level quiz on {subject} with exactly {num_questions} multiple-choice questions.

    INSTRUCTIONS:
    1. Each question should be appropriate for {level} level students.
    2. Each question must have exactly 4 answer options (A, B, C, D).
    3. Clearly indicate the correct answer for each question.
    4. Include a brief hint for each question to help students without giving away the answer.
    5. Cover diverse aspects of {subject} to ensure a comprehensive assessment.

    FORMAT YOUR RESPONSE AS JSON:
        '''json
        [
            {{
                "question": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "hint": "Brief helpful hint for this question",
                "explanation": "Brief explanation of why this answer is correct"
            }},
        ...
    ]
    '''
    IMPORTANT: Make sure to return valid JSON that can be parsed. Do not include any text outside the JSON array.
    """


def _create_fallback_quiz(subject, num_questions):
    """Helper function to create a fallback quiz if parsing fails"""
    logger.warning(f"Using fallback quiz for subject: {subject}")

    return [
        {
            "question": f"Sample {subject} Question #{i + 1}",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "This is a sample explanation."
        }
        for i in range(num_questions)
    ]


def _validate_quiz_data(quiz_data):
    """Helper function to validate quiz data structure"""

    if not isinstance(quiz_data, list):
        raise ValueError("Quiz data must be a list of questions.")
    
    for question in quiz_data:
        if not isinstance(question, dict):
            raise ValueError("Each quiz item must be a dictionary.")
        
        if not all(key in question for key in ["question", "options", "correct_answer"]):
            raise ValueError("Each quiz item must contain 'question', 'options', and 'correct_answer'")
        
        if not isinstance(question["options"], list) or len(question["options"]) != 4:
            raise ValueError("Each question must have exactly 4 options.")


def _parse_quiz_response(response_content, subject, num_questions):
    """Helper function to parse and validate the quiz response."""

    try:
        json_match = re.search(r'```json\s*(\[[\sS]*?\])\s*```', response_content)

        if json_match:
            quiz_json = json_match.group(1)
        else:
            json_match = re.search(r'\[\s*\{.*\}\s*\]', response_content, re.DOTALL)
            if json_match:
                quiz_json = json_match.group(0)
            else:
                quiz_json = response_content
        
        quiz_data = json.loads(quiz_json)

        _validate_quiz_data(quiz_data)

        if len(quiz_data) > num_questions:
            quiz_data = quiz_data[:num_questions]

        for question in quiz_data:
            if "explanation" not in question:
                question["explanation"] = f"The correct answer is {question['correct_answer']}."
            if "hint" not in question or not question["hint"]:
                question["hint"] = "Think carefully about the key concept here."
            
        return quiz_data
    
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error parsing quiz response: {str(e)}")

        return _create_fallback_quiz(subject, num_questions)


def generate_quiz(subject, level, num_questions=5, reveal_answer=True):
    """Generate quiz with multiple choice questions based on subject and level

    Args:
        subject (str): The subject of the quiz (e.g., Math, Science).
        level (str): The educational level (e.g., Beginner, Intermediate, Advanced).
        num_questions (int): Number of questions in the quiz.
        reveal_answer (bool): Whether to include correct answers and explanations in the response.

    Returns:
        dict: Contain the quiz data (list of questions) and formatted HTML if reveal_answer is True.
    """
    formatted_quiz = None
    try:
        llm = get_llm()

        prompt = _create_quiz_prompt(subject, level, num_questions)

        logger.info(f"Generating quiz for subject: {subject}, level: {level}, questions: {num_questions}")
        response = llm([HumanMessage(content=prompt)])

        quiz_data = _parse_quiz_response(response.content, subject, num_questions)

        if reveal_answer:
            formatted_quiz = _format_quiz_with_reveal(quiz_data)
            return {
                "quiz_data": quiz_data,
                "formatted_quiz": formatted_quiz
            }
        else:
            return {
                "quiz_data": quiz_data
            }
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise Exception(f"Failed to generate quiz: {str(e)}")


def _format_quiz_with_reveal(quiz_data):
    """Format quiz data into HTML with hidden answers that can be revealed on click
    
    Args:
        quiz_data (list): List of question dictionaries.

    Returns:
        str: HTML string with quiz questions and hidden answers.
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                color: white;
                background-color: #121212;
            }
            .quiz-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .question {
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #444;
                border-radius: 10px;
                background-color: #1e1e2f;
            }
            .question h3 {
                margin-top: 0;
            }
            .options label {
                display: block;
                margin-bottom: 8px;
                cursor: pointer;
            }
            .options input[type="radio"] {
                margin-right: 10px;
            }
            .feedback {
                margin-top: 10px;
                font-weight: bold;
            }
            .correct {
                color: #4CAF50;
            }
            .incorrect {
                color: #f44336;
            }
            .hint, .answer {
                display: none;
                margin-top: 10px;
                padding: 10px;
                background-color: #333;
                border-radius: 5px;
                border: 1px solid #555;
            }
            .btn {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
                margin-right: 10px;
                font-size: 14px;
            }
            .btn:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="quiz-container">
    """

    # For labeling options a, b, c, d
    option_labels = ['a', 'b', 'c', 'd']

    for idx, question in enumerate(quiz_data):
        html += f"""
            <div class="question" id="question-{idx}">
                <h3>Q{idx + 1}: {question['question']}</h3>
                <div class="options">
        """

        for i, option in enumerate(question['options']):
            html += f"""
                <label>
                    <input type="radio" name="q{idx}" value="{option}">
                    <strong>{option_labels[i]})</strong> {option}
                </label>
            """

        html += f"""
                </div>
                <button class="btn" onclick="checkAnswer({idx}, '{question['correct_answer']}')">Check Answer</button>
                <button class="btn" onclick="toggleHint({idx})">Hint</button>
                <button class="btn" onclick="toggleAnswer({idx})">Reveal Answer</button>

                <div class="feedback" id="feedback-{idx}"></div>

                <div class="hint" id="hint-{idx}">
                    <strong>Hint:</strong> {question.get('hint', 'No hint available for this question.')}
                </div>

                <div class="answer" id="answer-{idx}">
                    <p><strong>Correct Answer: </strong>{question['correct_answer']}</p>
                    <p><strong>Explanation: </strong>{question.get('explanation', '')}</p>
                </div>
            </div>
        """

    html += """
        </div>
        <script>
            function checkAnswer(qIdx, correctAnswer) {
                const options = document.getElementsByName('q' + qIdx);
                let selected = null;
                for (const opt of options) {
                    if (opt.checked) {
                        selected = opt.value;
                        break;
                    }
                }
                const feedbackEl = document.getElementById('feedback-' + qIdx);
                if (!selected) {
                    feedbackEl.innerHTML = '<span class="incorrect">Please select an answer before checking.</span>';
                    return;
                }
                if (selected === correctAnswer) {
                    feedbackEl.innerHTML = '<span class="correct">Correct! 🎉</span>';
                } else {
                    feedbackEl.innerHTML = '<span class="incorrect">Incorrect! Try again or reveal the answer.</span>';
                }
            }

            function toggleHint(qIdx) {
                const hintEl = document.getElementById('hint-' + qIdx);
                if (hintEl.style.display === 'block') {
                    hintEl.style.display = 'none';
                } else {
                    hintEl.style.display = 'block';
                }
            }

            function toggleAnswer(qIdx) {
                const answerEl = document.getElementById('answer-' + qIdx);
                if (answerEl.style.display === 'block') {
                    answerEl.style.display = 'none';
                } else {
                    answerEl.style.display = 'block';
                }
            }
        </script>
    </body>
    </html>
    """

    return html

def generate_quiz_html(quiz_data):  
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                color: white;
                background-color: #121212;
            }
            .quiz-container{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .question{
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #444;
                border-radius: 10px;
                background-color: #1e1e2f;
            }
            .question h3{
                margin-top: 0;
            }
            .answer{
                display: none;
                margin-top: 10px;
                padding: 10px;
                background-color: #333;
                border-radius: 5px;
                border: 1px solid #555;
            }
            .reveal-btn{
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
            }
            .reveal-btn:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="quiz-container">
    """

    for question in quiz_data:
        html += f"""
            <div class="question">
                <h3>{question['question']}</h3>
                <ul>
                    <li>{question['options'][0]}</li>
                    <li>{question['options'][1]}</li>
                    <li>{question['options'][2]}</li>
                    <li>{question['options'][3]}</li>
                </ul>
                <button class="reveal-btn" onclick="toggleAnswer(this)">Reveal Answer</button>
                <div class="answer">
                    <p><strong>Correct Answer: </strong>{question['correct_answer']}</p>
                    <p><strong>Explanation: </strong>{question['explanation']}</p>
                </div>
            </div>
        """

    html += """
        </div>
        <script>
            function toggleAnswer(button) {
                var answer = button.nextElementSibling;
                if (answer.style.display === "none") {
                    answer.style.display = "block";
                    button.innerText = "Hide Answer";
                } else {
                    answer.style.display = "none";
                    button.innerText = "Reveal Answer";
                }
            }
        </script>
    </body>
    </html>
    """

    return html

def export_quiz_to_html(quiz_data, file_path = "quiz.html"):
    """Export the formatted quiz to an HTML file .

    Args:
        quiz_data (list): List of question dictionaries.
        file_path (str): Path to save the HTML file.
    """
    try:
        html_content = _format_quiz_with_reveal(quiz_data)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"Quiz successfully exported to {file_path}")
        return True

    except Exception as e:
        logger.error(f"Error exporting quiz to HTML: {str(e)}")
        return False