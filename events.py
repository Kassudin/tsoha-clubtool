import users
from sqlalchemy import text
from db import db

def create_event(event_type, event_date, event_start_time, event_end_time, event_location, event_description, position_specific):
    sql = text("""
        INSERT INTO events 
        (event_type, event_date, event_start_time, event_end_time, 
        event_location, event_description, position_specific) 
        VALUES 
        (:event_type, :event_date, :event_start_time, :event_end_time, 
        :event_location, :event_description, :position_specific)
    """)
    db.session.execute(sql, {
        "event_type": event_type,
        "event_date": event_date,
        "event_start_time": event_start_time,
        "event_end_time": event_end_time,
        "event_location": event_location,
        "event_description": event_description,
        "position_specific": position_specific if position_specific else None
    })
    db.session.commit()
    return True

def get_list():
    sql = text("""
        SELECT e.id, e.event_type, e.event_date, e.event_start_time, e.event_end_time, 
        e.event_location, e.is_cancelled,
        COUNT(CASE WHEN er.status = 'IN' THEN 1 END) AS in_count,
        COUNT(CASE WHEN er.status = 'OUT' THEN 1 END) AS out_count,
        (SELECT status FROM event_registrations WHERE event_id = e.id 
        AND user_id = :user_id) AS current_status,
        e.position_specific
        FROM events e
        LEFT JOIN event_registrations er ON e.id = er.event_id
        WHERE e.position_specific IS NULL OR e.position_specific = :user_position
        GROUP BY e.id
        ORDER BY e.event_date ASC, e.event_start_time ASC
    """)
    result = db.session.execute(sql, {
        "user_id": users.user_id(), 
        "user_position": users.get_user_position(users.user_id())
    })
    return result.fetchall() 

def get_list_coach():
    sql = text("""
        SELECT e.id, e.event_type, e.event_date, e.event_start_time, e.event_end_time, 
        e.event_location, e.is_cancelled,
        COUNT(CASE WHEN er.status = 'IN' THEN 1 END) AS in_count,
        COUNT(CASE WHEN er.status = 'OUT' THEN 1 END) AS out_count,
        (SELECT status FROM event_registrations WHERE event_id = e.id 
        AND user_id = :user_id) AS current_status,
        e.position_specific
        FROM events e
        LEFT JOIN event_registrations er ON e.id = er.event_id
        GROUP BY e.id
        ORDER BY e.event_date ASC, e.event_start_time ASC
    """)
    result = db.session.execute(sql, {"user_id": users.user_id()})
    return result.fetchall()

def register_user_to_event(event_id, user_id, status, comment=None):
    sql = text("""
        INSERT INTO event_registrations (event_id, user_id, status, comment) 
        VALUES (:event_id, :user_id, :status, :comment)
        ON CONFLICT (event_id, user_id) 
        DO UPDATE SET status = EXCLUDED.status, comment = EXCLUDED.comment
    """)
    db.session.execute(sql, {
        "event_id": event_id,
        "user_id": user_id,
        "status": status,
        "comment": comment
    })
    db.session.commit()
    return True

def get_event_details(event_id, user_id):
    sql_event = text("""
        SELECT e.id, e.event_type, e.event_date, e.event_start_time, e.event_end_time, 
        e.event_location, e.event_description,
        (SELECT status FROM event_registrations WHERE event_id = e.id AND user_id = :user_id) AS current_status
        FROM events e
        WHERE e.id = :event_id
    """)
    event_info = db.session.execute(sql_event, {"event_id": event_id, "user_id": user_id}).fetchone()
    sql_registrations = text("""
        SELECT COALESCE(u.player_name, er.external_player) AS player_name, er.status, er.comment
        FROM event_registrations er
        LEFT JOIN users u ON u.id = er.user_id
        WHERE er.event_id = :event_id
    """)
    registrations = db.session.execute(sql_registrations, {"event_id": event_id}).fetchall()
    in_list = [f"{reg.player_name} ({reg.comment})" if reg.comment else reg.player_name for reg in registrations if reg.status == 'IN']
    out_list = [f"{reg.player_name} ({reg.comment})" if reg.comment else reg.player_name for reg in registrations if reg.status == 'OUT']
    return event_info, in_list, out_list

def get_registration_count(user_id):
    if users.is_coach():
        sql = text("""
            SELECT COUNT(*) 
            FROM event_registrations er
            JOIN events e ON er.event_id = e.id
            WHERE er.user_id = :user_id 
            AND e.is_cancelled = FALSE
        """)
        result = db.session.execute(sql, {"user_id": user_id})
    else:
        sql = text("""
            SELECT COUNT(*) 
            FROM event_registrations er
            JOIN events e ON er.event_id = e.id
            WHERE er.user_id = :user_id 
            AND e.is_cancelled = FALSE
            AND (e.position_specific IS NULL OR e.position_specific = :user_position)
        """)
        result = db.session.execute(sql, {
            "user_id": user_id, 
            "user_position": users.get_user_position(user_id)
        })
    registration_count = result.fetchone()[0]
    return registration_count

def get_total_events(user_id):
    if users.is_coach():
        sql = text("""
            SELECT COUNT(*) 
            FROM events 
            WHERE is_cancelled = FALSE
        """)
        result = db.session.execute(sql)
    else:
        sql = text("""
            SELECT COUNT(*) 
            FROM events 
            WHERE is_cancelled = FALSE
            AND (position_specific IS NULL OR position_specific = :user_position)
        """)
        result = db.session.execute(sql, {
            "user_position": users.get_user_position(user_id)
        })
    total_events = result.fetchone()[0]
    return total_events

def cancel_event(event_id):
    sql = text("UPDATE events SET is_cancelled = TRUE WHERE id = :event_id")
    db.session.execute(sql, {"event_id": event_id})
    db.session.commit()
    return True

def get_user_status(event_id, user_id):
    sql = text("""
        SELECT status FROM event_registrations 
        WHERE event_id = :event_id AND user_id = :user_id
    """)
    result = db.session.execute(sql, {"event_id": event_id, "user_id": user_id}).fetchone()
    if result:
        return result[0]
    return None

def get_event_id(event_id):
    sql = text(""" 
        SELECT id, event_type, event_date, event_start_time, event_end_time, event_location, event_description, position_specific
        FROM events 
        WHERE id = :event_id           
    """)
    return db.session.execute(sql, {"event_id": event_id}).fetchone()

def update_event_db(event_id, event_type, event_date, event_start_time, event_end_time, event_location, event_description, position_specific):
    sql = text("""
        UPDATE events SET event_type=:event_type, event_date=:event_date, event_start_time=:event_start_time,
        event_end_time=:event_end_time, event_location=:event_location, event_description=:event_description, position_specific=:position_specific
        WHERE id = :event_id
    """)
    position_specific = position_specific if position_specific else None
    db.session.execute(sql, {
        "event_id": event_id, 
        "event_type": event_type, 
        "event_date": event_date,
        "event_start_time": event_start_time, 
        "event_end_time": event_end_time, 
        "event_location": event_location, 
        "event_description": event_description, 
        "position_specific": position_specific
    })
    db.session.commit() 

def add_external_player_to_event(event_id, player_name):
    sql = text("""
        INSERT INTO event_registrations (event_id, external_player, status)
        VALUES (:event_id, :player_name, 'IN')
    """)
    db.session.execute(sql, {
        'event_id': event_id, 
        'player_name': player_name
    })
    db.session.commit()
