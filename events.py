from db import db
from sqlalchemy import text

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
    result = db.session.execute(text("SELECT id, event_type, event_date, event_start_time, event_end_time, event_location, event_description FROM events"))
    return result.fetchall()

def register_user_to_event(event_id, user_id, status):
    sql = text ("INSERT INTO event_registrations (event_id, user_id, status) VALUES (:event_id, :user_id, :status) ON CONFLICT (event_id, user_id) DO UPDATE SET status = EXCLUDED.status")
    db.session.execute(sql, {"event_id": event_id, "user_id": user_id, "status": status})
    db.session.commit()
    return True