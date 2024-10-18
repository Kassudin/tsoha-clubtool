from app import app
from flask import render_template, request, redirect
import users, events, messages
import datetime

# Route to front page
@app.route("/")
def index():
    if not users.user_id:
        return render_template ("error.html", message="Ei oikeutta nähdä sivua")
    if users.is_coach():
        event_list = events.get_list_coach()
    else:
        event_list = events.get_list()
    user_id = users.user_id()
    event_registration_count, total_events = events.get_registration_count(user_id), events.get_total_events(user_id)
    welcome_message = f"Hei {users.player_name(user_id)}, olet ilmoittautunut {event_registration_count}/{total_events} tapahtumaan!"
    return render_template("index.html", events = event_list, welcome_message=welcome_message)   
      
# Route to login page 
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        player_name = request.form["player_name"]
        password = request.form["password"]
        if users.login(player_name, password):
            return redirect("/")
        return render_template("error.html", message="Väärä tunnus tai salasana")
                
# Route to logout user
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

# Route to user registration
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        player_name = request.form["player_name"]
        password1= request.form["password1"]
        password2= request.form["password2"]
        player_position=request.form["player_position"]
        player_number=request.form["player_number"]
        if password1!=password2:
            return render_template("error.html", message="Salasanat eroavat")
        if not 3 <= len(player_name) <= 30:
            return render_template("error.html", message="Virheellinen nimi")
        allowed_positions = ["maalivahti", "puolustaja", "keskikenttä", "hyökkääjä"]
        if player_position not in allowed_positions:
            return render_template("error.html", message="Virheellinen pelipaikka")
        if not player_number.isdigit() or not (1 <= int(player_number) <= 99):
            return render_template("error.html", message="Pelaajanumeron tulee olla luku väliltä 1-99")
        if users.register(player_name, password1, player_position, player_number):
            return redirect("/")
        return render_template("error.html", message="Tapahtui virhe rekisteröitymisessä")

# Route to event creation page
@app.route("/new_event")
def new():
    allow = False
    if users.is_coach():
        allow = True
    if not allow:
        return render_template ("error.html", message="Ei oikeutta nähdä sivua")
    return render_template("new_event.html")

# Route to create a new event
@app.route("/new_event", methods=["POST"])
def create_event():
    if not users.is_coach():
        return render_template("error.html", message="Vain valmentajat voivat luoda tapahtumia.")
    event_type = request.form.get("event_type")
    event_date = request.form.get("event_date")
    event_start_time = request.form.get("event_start_time")
    event_end_time = request.form.get("event_end_time")
    event_location = request.form.get("event_location")
    event_description = request.form.get("event_description", "")  
    position_specific = request.form.get("position_specific", None)
    allowed_event_types = ["harjoitus", "ottelu", "muu"]
    if event_type not in allowed_event_types:
        return render_template("error.html", message="Virheellinen tapahtumatyyppi")
    if not event_date:
        return render_template("error.html", message="Päivämäärä on pakollinen")
    if not event_start_time or not event_end_time:
        return render_template("error.html", message="Aloitus- ja lopetusaika ovat pakollisia")
    if not 1 <= len(event_location) <= 100:
        return render_template("error.html", message="Tapahtumapaikan tulee olla 1-100 merkkiä pitkä")
    if len(event_description) > 100:
        return render_template("error.html", message="Kuvaus on liian pitkä (max 100 merkkiä)")
    success = events.create_event(event_type, event_date, event_start_time, event_end_time, event_location, event_description, position_specific)
    if success:
        return redirect("/")
    return render_template("error.html", message="Tapahtuman luominen epäonnistui")

# Route to register the user to the event  
@app.route("/event_registration", methods=["POST"])
def event_registration():
    if not users.user_id():
        return redirect("/login")
    event_id = request.form["event_id"]
    status = request.form["status"] 
    user_id = users.user_id()
    events.register_user_to_event(event_id, user_id, status)
    return redirect("/")

# Route to add a comment
@app.route("/add_comment", methods=["POST"])
def add_comment():
    if not users.user_id():
        return redirect("/login")
    event_id = request.form["event_id"]
    comment = request.form.get("comment", "")
    user_id = users.user_id()
    status = events.get_user_status(event_id, user_id)
    if status not in ['IN', 'OUT']:
        return render_template("error.html", message="Et voi lähettää kommenttia, ellet ole ilmoittautunut tapahtumaan.")
    if not 1 <= len(comment) <= 30:
        return render_template("error.html", message="Kommentin tulee olla 1-30 merkkiä pitkä.")
    events.register_user_to_event(event_id, user_id, status, comment)
    return redirect(f"/event/{event_id}")

# Route to event details page
@app.route("/event/<int:event_id>")
def event_details(event_id):
    user_id = users.user_id()
    event_info, in_list, out_list = events.get_event_details(event_id, user_id)
    return render_template("event_details.html", event=event_info, in_list=in_list, out_list=out_list)

# Route to message creation page
@app.route("/send_message")
def send_message_form():
    if not users.user_id:
        return redirect('/login')
    if not users.is_coach():
        return render_template("error.html", message="Vain valmentajat voivat lähettää viestejä.")
    return render_template("send_message.html")

# Route to send a new message
@app.route("/send_message", methods=["POST"])
def send_message():
    if not users.user_id():
        return redirect('/login')
    if not users.is_coach():
        return render_template("error.html", message="Vain valmentajat voivat lähettää viestejä.")
    content = request.form.get("content")
    if not 1 <= len(content) <= 100:
        return render_template("error.html", message="Viestin tulee olla 1-100 merkkiä pitkä")
    success = messages.send_message(content)
    if success:
        return redirect("/messages")
    else:
        return render_template("error.html", message="Viestin lähetys epäonnistui.")

# Route to view the messages 
@app.route("/messages")
def view_messages():
    if not users.user_id():
        return redirect('/login')
    message_list = messages.get_all_messages()
    return render_template("messages.html", messages=message_list)

@app.route("/cancel_event/<int:event_id>", methods=["POST"])
def cancel_event(event_id):
    if not users.is_coach():
        return render_template("error.html", message="Vain valmentajat voivat peruuttaa tapahtumia")
    if events.cancel_event(event_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Tapahtui virhe peruuttamisessa")

@app.route("/edit_event/<int:event_id>")
def edit_event(event_id):
    if not users.is_coach():
        return render_template("error.html", message="Vain valmentajat voivat muokata tapahtumia")
    event = events.get_event_id(event_id)
    if event:
        return render_template("edit_event.html", event=event)
    else:
        return render_template("error.html", message= "Tapahtumaa ei löydy")

@app.route("/update_event/<int:event_id>", methods=["POST"])
def update_event(event_id):
    if not users.is_coach():
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    event_type = request.form["event_type"]
    event_date = request.form["event_date"]
    event_start_time = request.form["event_start_time"]
    event_end_time = request.form["event_end_time"]
    event_location = request.form["event_location"]
    event_description = request.form["event_description"]
    position_specific = request.form["position_specific"]
    events.update_event_db(event_id, event_type, event_date, event_start_time, event_end_time, event_location, event_description, position_specific)
    return redirect("/")

@app.route("/add_external_player_to_event", methods=["POST"])
def add_external_player_to_event():
    if not users.is_coach():
        return render_template("error.html", message="Ei oikeutta lisätä ulkopuolista pelaajaa")
    event_id = request.form.get("event_id")
    external_player = request.form.get("external_player")
    if not 2 <= len(external_player) <= 30:
        return render_template("error.html", message="Virheellinen nimi")
    events.add_external_player_to_event(event_id, external_player)
    return redirect(f"/event/{event_id}")   