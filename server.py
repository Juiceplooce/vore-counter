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

        try:
            res = requests.get(url, timeout=10)

            if res.status_code == 200 and "application/json" in res.headers.get("Content-Type", ""):
                data = res.json()
                count += data.get("metadata", {}).get("total_results", 0)
            else:
                print(f"Bad response: status={res.status_code}, content-type={res.headers.get('Content-Type')}")
        except Exception as e:
            print(f"Error during request: {e}")

    return count

@app.route("/vorecount")
def vore_count():
    count = get_vore_mentions()
    return jsonify({"vore_mentions_last_24h": count})

if __name__ == "__main__":
    app.run()
