from flask import Flask, jsonify
import datetime
import requests

app = Flask(__name__)

def get_vore_mentions():
    now = int(datetime.datetime.utcnow().timestamp())
    one_hour = 3600
    count = 0
    for i in range(24):
        start = now - ((i + 1) * one_hour)
        end = now - (i * one_hour)
        url = f"https://api.pushshift.io/reddit/comment/search/?q=vore&after={start}&before={end}&size=0&metadata=true"
        res = requests.get(url).json()
        count += res.get("metadata", {}).get("total_results", 0)
    return count

@app.route("/vorecount")
def vore_count():
    count = get_vore_mentions()
    return jsonify({"vore_mentions_last_24h": count})

if __name__ == "__main__":
    app.run()
