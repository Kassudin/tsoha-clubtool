from app import app
from flask import render_template, request, redirect
import users, events

# Route to front page
@app.route("/")
def index():
    event_list = events.get_list()
    return render_template("index.html", events = event_list)   
        
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
@app.route("/new_event", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        event_type = request.form.get("event_type")
        event_date = request.form.get("event_date")
        event_start_time = request.form.get("event_start_time")
        event_end_time = request.form.get("event_end_time")
        event_location = request.form.get("event_location")
        event_description = request.form.get("event_description", "")  
        success = events.create_event(event_type, event_date, event_start_time, event_end_time, event_location, event_description)
        if success:
            return redirect("/")
        return render_template("error.html", message="Tapahtuman luominen epäonnistui.")

# Route to register the user to the event   
@app.route("/event_registration", methods=["POST"])
def event_registration():
    if not users.user_id:
        return redirect("/login")
    event_id = request.form["event_id"]
    status = request.form["status"]
    user_id = users.user_id()
    events.register_user_to_event(event_id, user_id, status)
    return redirect("/")