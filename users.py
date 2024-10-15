from db import db 
from sqlalchemy import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(player_name, password):
	sql = text ("SELECT id, password, coach FROM users WHERE player_name=:player_name")
	result = db.session.execute(sql, {"player_name": player_name})
	user=result.fetchone()
	if not user:
		return False
	else:
		if check_password_hash(user.password, password):
			session["user_id"] = user.id
			session["coach"] = user.coach
			return True
		else:
			return False
		
def logout():
	del session["user_id"]

def register(player_name, password, player_position, player_number):
    hash_value = generate_password_hash(password)
    try:
        sql_users = text("INSERT INTO users (player_name, password) VALUES (:player_name, :password) RETURNING id")
        result = db.session.execute(sql_users, {"player_name": player_name, "password": hash_value})
        user_id = result.fetchone()[0]
        sql_details = text("INSERT INTO user_details (user_id, player_position, player_number) VALUES (:user_id, :player_position, :player_number)")
        db.session.execute(sql_details, {"user_id": user_id, "player_position": player_position, "player_number": player_number})
        db.session.commit()
    except: 
        return False
    return login(player_name, password)

def user_id():
	return session.get("user_id", 0)

def is_coach():
	return session.get("coach", False)

def player_name(user_id):
    sql = text("SELECT player_name FROM users WHERE id = :user_id")
    result = db.session.execute(sql, {'user_id': user_id})
    user = result.fetchone()
    return user.player_name if user else None


def get_user_position(user_id):
    sql = text("""
        SELECT ud.player_position
        FROM user_details ud
        JOIN users u ON ud.user_id = u.id
        WHERE u.id = :user_id
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    user_position = result.fetchone()
    if user_position:
        return user_position[0]
    else:
        return None
