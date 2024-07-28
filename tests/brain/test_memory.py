import pytest
import hashlib
from regdbot.brain.memory import History, Problem
import datetime

def test_setup_db():
    history = History()
    assert history.engine is not None

def test_memorize():
    history = History(dburl='sqlite://')
    session_id = hashlib.md5(f"{datetime.datetime.now()}{'test'}{'gpt'}".encode()).hexdigest()
    question = "how can I print a string in Python?"
    code = "print('Hello, World!')"
    explanation = "This code snippet prints a string."
    context = "Programming languages"
    memory = history.memorize(session_id, question, code, explanation, context)
    assert memory is not None
    assert memory.id is not None
    assert memory.session_id == session_id
    assert memory.question == question
    assert memory.code == code
    assert memory.explanation == explanation
    assert memory.context == context

def test_recall():
    history = History(dburl='sqlite://')
    session_id = hashlib.md5(f"{datetime.datetime.now()}{'test'}{'gpt'}".encode()).hexdigest()
    question = "How can I print a string in Python?"
    code = "print('Hello, World!')"
    explanation = "this code snippet prints a string."
    context = "Programming languages"
    memory = history.memorize(session_id, question, code, explanation, context)
    results = history.recall(session_id)
    assert results is not None
    for result in results:
        assert isinstance(result, Problem)
        assert result.session_id == session_id