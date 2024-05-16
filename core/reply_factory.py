
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not answer:
        return False, "Answer cannot be empty"

    session["answers"] = session.get("answers", {})
    session["answers"][current_question_id] = answer
    session.save()

    return True, ""



def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0  

    try:
        current_question_index = PYTHON_QUESTION_LIST.index(current_question_id)
    except ValueError:
        return None, None 

    if current_question_index + 1 < len(PYTHON_QUESTION_LIST):
        next_question_index = current_question_index + 1
        return PYTHON_QUESTION_LIST[next_question_index], next_question_index
    else:
        return None, None 



def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    for question_id, correct_answer in PYTHON_QUESTION_LIST.items():
        user_answer = session.get("answers", {}).get(question_id)
        if user_answer == correct_answer:
            correct_answers += 1

    score = (correct_answers / total_questions) * 100

    final_response = f"Your quiz result:\nTotal Questions: {total_questions}\nCorrect Answers: {correct_answers}\nScore: {score:.2f}%"

    return final_response

