from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GOOGLE_API_KEY = "INSERT_HERE"

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    user_lat = None
    user_lng = None
    radius_km = 20  # default radius

    if request.method == "POST":
        user_lat = request.form.get("lat")
        user_lng = request.form.get("lng")
        preferred_time = request.form.get("time")
        date = request.form.get("date")
        radius_km = request.form.get("radius") or 20

        if user_lat and user_lng:
            user_lat = float(user_lat)
            user_lng = float(user_lng)

            # Google Places Nearby Search
            endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": f"{user_lat},{user_lng}",
                "radius": int(radius_km) * 1000,
                "type": "golf_course",
                "keyword": "golf",
                "key": GOOGLE_API_KEY
            }

            response = requests.get(endpoint, params=params).json()
            print(response)

            for place in response.get("results", []):
                place_types = place.get("types", [])
                name = place.get("name", "").lower()
                if "golf" in name or "golf_course" in place_types:
                    results.append({
                        "club": place["name"],
                        "lat": place["geometry"]["location"]["lat"],
                        "lng": place["geometry"]["location"]["lng"]
                    })

    return render_template(
        "index.html",
        results=results,
        user_lat=user_lat,
        user_lng=user_lng,
        radius_km=radius_km,
        today=request.form.get("date")
    )

if __name__ == "__main__":
    app.run(debug=True)
