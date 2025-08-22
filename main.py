from flask import Flask, render_template, request

app = Flask(__name__)

# Mock data (you’ll replace this with real API/database later)
clubs = {
    "Dublin Golf Club": ["08:00", "10:00", "13:30"],
    "Phoenix Park Golf": ["09:15", "11:00", "14:00"],
    "Clontarf Golf": ["07:30", "12:00", "15:45"]
}

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        preferred_time = request.form.get("time")
        for club, times in clubs.items():
            for t in times:
                if preferred_time <= t:  # simple filter
                    results.append((club, t))
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
