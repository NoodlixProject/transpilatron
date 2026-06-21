import requests
import os
ENDPOINT = "http://transpilatron-tememetry.vercel.app/ping"
message_seen = False

def report(event_type: str, version: str) -> None:
    global message_seen
    if os.environ.get("TRANSPILATRON_DISABLE_TELEMETRY") == "1":
        return
    
    if not message_seen:
        print("Transpilatron collects anonymous telemetry. Disable with TRANSPILATRON_DISABLE_TELEMETRY=1")
        message_seen = True

    try:
        requests.post(ENDPOINT, json={
            "type": event_type,
            "version": version,
        }, timeout=2)
    except:
        pass  