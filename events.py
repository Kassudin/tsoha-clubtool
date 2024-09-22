from db import db
from sqlalchemy import text
import users

def create_event(event_type, event_date, event_start_time, event_end_time, event_location, event_description):
    sql = text("INSERT INTO events (event_type, event_date, event_start_time, event_end_time, event_location, event_description) VALUES (:event_type, :event_date, :event_start_time, :event_end_time, :event_location, :event_description)")
    db.session.execute(sql, {
            "event_type": event_type,
            "event_date": event_date,
            "event_start_time": event_start_time,
            "event_end_time": event_end_time,
            "event_location": event_location,
            "event_description": event_description})
    db.session.commit()
    return True

def get_list():
    sql = text("""
        SELECT e.id, e.event_type, e.event_date, e.event_start_time, e.event_end_time, e.event_location, e.event_description,
        COUNT(CASE WHEN er.status = 'IN' THEN 1 END) AS in_count,
        COUNT(CASE WHEN er.status = 'OUT' THEN 1 END) AS out_count,
        (SELECT status FROM event_registrations WHERE event_id = e.id AND user_id = :user_id) AS current_status                             
        FROM events e
        LEFT JOIN event_registrations er ON e.id = er.event_id
        GROUP BY e.id
        ORDER BY e.event_date ASC, e.event_start_time ASC
    """)
    result = db.session.execute (sql, {"user_id" : users.user_id()})
    return result.fetchall() 

def register_user_to_event(event_id, user_id, status):
    sql = text ("INSERT INTO event_registrations (event_id, user_id, status) VALUES (:event_id, :user_id, :status) ON CONFLICT (event_id, user_id) DO UPDATE SET status = EXCLUDED.status")
    db.session.execute(sql, {"event_id": event_id, "user_id": user_id, "status": status})
    db.session.commit()
    return True