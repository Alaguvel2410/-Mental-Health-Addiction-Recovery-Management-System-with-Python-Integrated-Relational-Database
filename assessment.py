from database import get_connection
def create_assessment(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """INSERT INTO assessment 
               (user_id, assessment_date) 
               VALUES (%s, CURDATE())"""

    cursor.execute(query, (user_id,))
    conn.commit()
    assessment_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return assessment_id

def get_questions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question_id, question_text FROM questions")
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return questions


def get_options():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT option_id, option_text FROM options_table")
    options = cursor.fetchall()
    cursor.close()
    conn.close()
    return options


def save_response(assessment_id, question_id, option_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO responses 
               (assessment_id, question_id, option_id) 
               VALUES (%s, %s, %s)"""
    cursor.execute(query, (assessment_id, question_id, option_id))
    conn.commit()
    cursor.close()
    conn.close()
