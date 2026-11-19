"""In-memory bounded telemetry; no question content or bearer tokens stored."""
from collections import deque
from threading import Lock
from time import time
EVENTS=deque(maxlen=500)
LOCK=Lock()
def record(route, latency_ms, status, mode=None):
    with LOCK:
        EVENTS.append({"time":round(time()),"route":route,"latency_ms":round(latency_ms,2),"status":status,"mode":mode})
def summary():
    with LOCK: events=list(EVENTS)
    return {"count":len(events),"avg_latency_ms":round(sum(e["latency_ms"] for e in events)/len(events),2) if events else 0,
            "errors":sum(e["status"]>=400 for e in events),"recent":events[-20:]}
