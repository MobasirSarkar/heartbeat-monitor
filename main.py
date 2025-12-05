import json
from heart_monitor import detect_alerts

EXPECTED_INTERVAL: int = 60
ALLOWED_MISSES: int = 3
EVENT_FILE: str = "events.json"


def main():
    with open(EVENT_FILE, "r") as f:
        data = json.load(f)

    alerts = detect_alerts(data, EXPECTED_INTERVAL, ALLOWED_MISSES)
    print(json.dumps(alerts, indent=4))


if __name__ == "__main__":
    main()
