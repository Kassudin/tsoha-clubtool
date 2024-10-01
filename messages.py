from db import db
import datetime
from sqlalchemy import text
import users

def send_message(content):
    user_id = users.user_id()
    sql = text("""
        INSERT INTO messages (user_id, content, sent_at)
        VALUES (:user_id, :content, :sent_at)
    """)
    db.session.execute(sql, {
        "user_id": user_id,
        "content": content,
        "sent_at": datetime.datetime.now()
    })
    db.session.commit()
    return True

def get_all_messages():
    sql =  text ("""
    SELECT m.content, m.sent_at, u.player_name 
    FROM messages m
    JOIN users u on m.user_id = u.id
    ORDER BY m.sent_at DESC            
    """)
    return db.session.execute(sql).fetchall()