import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_should_create_question_with_default_values():
    question = Question(title='A valid title')
    
    assert question.points == 1
    assert question.max_selections == 1
    assert question.id is not None

def test_should_raise_exception_for_empty_title():
    with pytest.raises(Exception, match='Title cannot be empty'):
        Question(title='')

def test_should_raise_exception_for_points_out_of_bounds():
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='Valid title', points=0)

def test_should_raise_exception_for_empty_choice_text():
    question = Question(title='Valid title')
    
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice(text='')

def test_should_raise_exception_for_too_long_choice_text():
    question = Question(title='Valid title')
    long_text = 'a' * 101
    
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice(text=long_text)


def test_should_add_a_choice_correctly():
    question = Question(title='What is the color of the sky?')
    
    question.add_choice('Blue', is_correct=True)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == 'Blue'
    assert question.choices[0].is_correct is True
    assert question.choices[0].id == 1

def test_should_remove_a_choice_by_id():
    question = Question(title='Programming Languages')
    question.add_choice('Python') # id=1
    question.add_choice('Java')   # id=2
    question.add_choice('C++')    # id=3
    

    question.remove_choice_by_id(2) # Remove 'Java'
    
    assert len(question.choices) == 2
    remaining_ids = [choice.id for choice in question.choices]
    assert remaining_ids == [1, 3]

def test_should_set_correct_choices():
    question = Question(title='Which of these are vowels?')
    question.add_choice('A') # id=1
    question.add_choice('B') # id=2
    question.add_choice('C') # id=3
    
    question.set_correct_choices([1])
    
    assert question.choices[0].is_correct is True  # Choice 'A'
    assert question.choices[1].is_correct is False # Choice 'B'
    assert question.choices[2].is_correct is False # Choice 'C'

def test_should_return_correct_id_on_correct_selected_choices():
    question = Question(title='Capital of France')
    question.add_choice('Berlin')       # id=1
    question.add_choice('Paris', is_correct=True) # id=2
    
    result = question.correct_selected_choices([2]) # User selects 'Paris'
    
    assert result == [2]

def test_should_return_empty_list_for_incorrect_selection():
    question = Question(title='Capital of Japan')
    question.add_choice('Beijing')      # id=1
    question.add_choice('Tokyo', is_correct=True) # id=2
    
    result = question.correct_selected_choices([1]) # User selects 'Beijing'
    
    assert result == []

@pytest.fixture
def multi_correct_question():
    """
    Provides a Question with 4 choices, where 2 are correct (IDs 2 and 4),
    and max_selections is set to 2.
    """
    question = Question(title='Which languages are statically typed?', points=10, max_selections=2)
    question.add_choice('Python')  # id=1
    question.add_choice('Java', is_correct=True)    # id=2
    question.add_choice('Ruby')    # id=3
    question.add_choice('C#', is_correct=True)      # id=4
    return question

def test_should_return_all_correct_ids_for_multiple_selections(multi_correct_question):
    selected_ids = [2, 4]
    result = multi_correct_question.correct_selected_choices(selected_ids)
    
    assert set(result) == {2, 4}

def test_should_return_partial_correct_ids_for_mixed_selections(multi_correct_question):
    selected_ids = [2, 3]
    result = multi_correct_question.correct_selected_choices(selected_ids)
    
    assert result == [2]