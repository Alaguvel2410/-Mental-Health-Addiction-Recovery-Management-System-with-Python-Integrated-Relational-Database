from database import get_connection

def get_result(assessment_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT 
                r.total_score,
                r.addiction_level,
                r.message,
                GROUP_CONCAT(t.tip_text SEPARATOR ' | ') AS tips
               FROM results r
               LEFT JOIN tips t 
               ON r.addiction_level = t.addiction_level
               WHERE r.assessment_id = %s
               GROUP BY r.assessment_id"""

    cursor.execute(query, (assessment_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result
