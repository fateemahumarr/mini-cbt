from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from models import Question, CBTStack

app = Flask(__name__)
app.secret_key = 'mini_cbt_super_secret_key'

# Global state for simplicity (fulfills requirements)
questions = [
    Question("What does HTML stand for?", ["Hyper Text Preprocessor", "Hyper Text Markup Language", "Hyper Tool Multi Language", "Hyperlink and Text Markup Language"], "Hyper Text Markup Language", 10),
    Question("Which of the following is a Python web framework?", ["React", "Angular", "Flask", "Vue"], "Flask", 10),
    Question("What is the time complexity of pushing to a Stack?", ["O(1)", "O(N)", "O(log N)", "O(N^2)"], "O(1)", 10),
    Question("In OOP, what concept restricts direct access to some of an object's components?", ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"], "Encapsulation", 10),
    Question("Which language is primarily used for adding interactivity to web pages?", ["HTML", "CSS", "JavaScript", "Python"], "JavaScript", 10),
    Question("What is a common use for the 'sudo' command in Linux?", ["To switch users", "To execute commands with administrative privileges", "To search for files", "To install software"], "To execute commands with administrative privileges", 10),
    Question("Which of these data structures acts like a queue in a supermarket?", ["Stack", "Queue", "Tree", "Graph"], "Queue", 10),
    Question("What does SQL stand for?", ["Structured Query Language", "Sequential Query Language", "Structured Question Language", "System Query Language"], "Structured Query Language", 10),
    Question("Which Git command is used to record changes to the repository?", ["git add", "git commit", "git push", "git status"], "git commit", 10),
    Question("What is the primary function of CSS?", ["Structuring web content", "Adding interactivity", "Styling and layout of web pages", "Server-side routing"], "Styling and layout of web pages", 10),
]

history_stack = CBTStack()

@app.route('/')
def home():
    # Reset session and stack when starting from home
    session['current_q'] = 0
    session['score'] = 0
    global history_stack
    history_stack = CBTStack()
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    current_q_idx = session.get('current_q', 0)
    
    # If we somehow bypassed the end, go to result
    if current_q_idx >= len(questions):
        return redirect(url_for('result'))
        
    question = questions[current_q_idx]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        
        # Check answer using our OOP model
        is_correct = question.check_answer(user_answer)
        
        if is_correct:
            session['score'] = session.get('score', 0) + question.points
            
        # Push to Stack (Data Structure requirement)
        history_stack.push({
            'question_text': question.text,
            'user_answer': user_answer,
            'correct_answer': question.correct_answer,
            'is_correct': is_correct
        })
        
        # Move to next question
        session['current_q'] = current_q_idx + 1
        
        if session['current_q'] >= len(questions):
            return redirect(url_for('result'))
            
        return redirect(url_for('quiz'))

    # GET request: render the question
    progress = (current_q_idx / len(questions)) * 100
    is_last = current_q_idx == len(questions) - 1
    
    return render_template(
        'quiz.html',
        question=question.get_formatted_question(),
        current_q_number=current_q_idx + 1,
        total_q=len(questions),
        progress=progress,
        is_last=is_last,
        history=history_stack.get_history()
    )

@app.route('/result')
def result():
    # API requirement: datatime.now()
    completion_time = datetime.now().strftime("%B %d, %Y at %I:%M:%S %p")
    
    score = session.get('score', 0)
    total_points = sum(q.points for q in questions)
    
    return render_template(
        'result.html',
        score=score,
        total_points=total_points,
        total_questions=len(questions),
        timestamp=completion_time,
        history=history_stack.get_history()
    )

if __name__ == '__main__':
    app.run(debug=True)
