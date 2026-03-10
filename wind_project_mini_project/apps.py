from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Your OpenWeatherMap API key (keep this safe for production!)
OPENWEATHER_API_KEY = "YOUR_API_KEY"

# Custom filter to join dicts or lists
@app.template_filter("join_filter")
def join_filter(value, delimiter=", "):
    if isinstance(value, dict):
        return delimiter.join([str(v) for v in value.values()])
    elif isinstance(value, list):
        return delimiter.join([str(v) for v in value])
    return str(value)

# Comma filter for large numbers
@app.template_filter("comma")
def comma_filter(value):
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value

@app.route("/")
def index():
    with open("static/data/countries.json") as f:
        country_list = json.load(f)
    return render_template("index.html", countries=country_list, title="WIND - Home")

@app.route("/country", methods=["GET", "POST"])
def country_info():
    # Support GET or POST
    country_name = request.args.get("country") or request.form.get("country")
    if not country_name:
        return render_template("country.html", error="No country provided")

    try:
        # Country data
        resp = requests.get(f"")
        resp.raise_for_status()
        country_data = resp.json()[0]

        # Weather for capital
        capital = country_data['capital'][0]
        weather_resp = requests.get(
            "",
            params={"q": capital, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        )
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        # Map coordinates
        lat, lon = country_data["latlng"]

        return render_template(
            "country.html",
            country=country_data,
            weather=weather_data,
            latitude=lat,
            longitude=lon
        )

    except Exception as e:
        print("Error:", e)
        return render_template("country.html", error="Could not retrieve data. Please check the country name.")

@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q", "").lower()
    with open("static/data/countries.json") as f:
        country_list = json.load(f)
    suggestions = [c for c in country_list if c.lower().startswith(query)]
    return jsonify(suggestions)

@app.route("/converter", methods=["GET", "POST"])
def converter():
    result = None
    symbol = ""
    chart_data = None

    # Currency names
    currencies = {
        "USD": "US Dollar",
        "EUR": "Euro",
        "INR": "Indian Rupee",
        "JPY": "Japanese Yen",
        "GBP": "British Pound",
        "AUD": "Australian Dollar",
        "CAD": "Canadian Dollar",
        "CHF": "Swiss Franc"
    }

    # Currency symbols
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "INR": "₹",
        "JPY": "¥",
        "GBP": "£",
        "AUD": "A$",
        "CAD": "C$",
        "CHF": "CHF"
    }

    from_currency = to_currency = amount = None

    if request.method == "POST":
        from_currency = request.form["from_currency"].upper()
        to_currency = request.form["to_currency"].upper()
        amount = request.form["amount"]

        try:
            amount = float(amount)

            # ✅ Conversion request
            api_url = f""
            response = requests.get(api_url)
            data = response.json()
            result = data["rates"][to_currency]

            # ✅ Historical chart data (7 days)
            from datetime import datetime, timedelta
            end_date = datetime.today().date()
            start_date = end_date - timedelta(days=7)

            chart_api = f""
            chart_resp = requests.get(chart_api)
            chart_json = chart_resp.json()

            chart_data = {
                "dates": list(chart_json["rates"].keys()),
                "rates": [v[to_currency] for v in chart_json["rates"].values()],
                "from_currency": from_currency,
                "to_currency": to_currency
            }

            symbol = currency_symbols.get(to_currency, to_currency)

        except Exception as e:
            result = f"Error: {e}"

    return render_template(
        "converter.html",
        result=result,
        symbol=symbol,
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        currencies=currencies,
        chart_data=chart_data
    )





if __name__ == "__main__":
    app.run(debug=True)
