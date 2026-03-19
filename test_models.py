from models import Question, CBTStack

def test_question_class():
    q = Question("What is 2 + 2?", ["3", "4", "5", "6"], "4", 10)
    
    # Test checking answer
    assert q.check_answer("4") == True, "Should be True for correct answer"
    assert q.check_answer(" 4 ") == True, "Should handle whitespace"
    assert q.check_answer("3") == False, "Should be False for incorrect answer"
    
    # Test formatted question
    formatted = q.get_formatted_question()
    assert formatted['text'] == "What is 2 + 2?"
    assert formatted['points'] == 10
    assert len(formatted['options']) == 4
    
    print("Question class tests passed!")

def test_stack_class():
    stack = CBTStack()
    
    assert stack.is_empty() == True
    
    stack.push({"question": "Q1", "answer": "A1"})
    stack.push({"question": "Q2", "answer": "A2"})
    
    assert stack.is_empty() == False
    assert stack.peek() == {"question": "Q2", "answer": "A2"}
    
    history = stack.get_history()
    assert history[0] == {"question": "Q2", "answer": "A2"}
    assert history[1] == {"question": "Q1", "answer": "A1"}
    
    popped = stack.pop()
    assert popped == {"question": "Q2", "answer": "A2"}
    assert stack.peek() == {"question": "Q1", "answer": "A1"}
    
    print("CBTStack tests passed!")

if __name__ == "__main__":
    test_question_class()
    test_stack_class()
    print("All backend model tests passed successfully.")
