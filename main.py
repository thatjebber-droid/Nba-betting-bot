
import requests

# TELEGRAM FUNCTION
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

# CONFIG (pull from Replit secrets)
import os
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def odds_to_prob(o):
    return 100/(o+100) if o > 0 else -o/(-o+100)

def get_odds():
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
    return requests.get(url, params={
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "h2h"
    }).json()

def run():
    bets = []

    for g in get_odds():
        for b in g["bookmakers"]:
            for m in b["markets"]:
                for o in m["outcomes"]:

                    prob = 0.55  # placeholder model
                    implied = odds_to_prob(o["price"])
                    edge = prob - implied

                    if edge > 0.05:
                        bets.append(
                            f"{o['name']} ({o['price']}) edge {round(edge,3)}"
                        )

    msg = "NBA PICKS:\n" + "\n".join(bets[:5]) if bets else "No bets today"

    send_telegram(msg)
    print(msg)

run()