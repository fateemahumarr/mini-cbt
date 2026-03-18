class Question:
    def __init__(self, text, options, correct_answer, points):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer
        self.points = points

    def check_answer(self, user_input):
        return str(user_input).strip().lower() == str(self.correct_answer).strip().lower()

    def get_formatted_question(self):
        return {
            'text': self.text,
            'options': self.options,
            'points': self.points
        }

class CBTStack:
    """A LIFO stack implementation to store user's recent attempts/review history."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def get_history(self):
        """Return history from most recent to oldest (LIFO order)."""
        return self.items[::-1]
