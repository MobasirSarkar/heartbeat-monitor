from __future__ import annotations
import heapq
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any

ISO8601 = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class Event:
    service: str
    timestamp: datetime


def parse_event(raw: Dict[str, Any]) -> Event | None:
    """
    Safetly parse an event. Return None if malformed.
    Malformed events must be ignored completely.
    """

    try:
        service = raw["service"]
        ts = datetime.strptime(raw["timestamp"], ISO8601)
        return Event(service=service, timestamp=ts)
    except Exception:
        return None


# def detect_alerts(
#    events: List[Dict[str, Any]], expected_interval_seconds: int, allowed_misses: int
# ) -> List[Dict[str, str]]:
#    """
#    Alert Detection Algorithm:
#      - it sort events per service.
#      - track expected heartbeats
#      - trigger alert on 3 consecutive missed intervals
#      - alert timestamp = first missed hearbeat occurrence
#    """
#
#    interval = timedelta(seconds=expected_interval_seconds)
#    threshold_gap = interval * (allowed_misses + 1)
#
#    services = defaultdict(list)
#    for raw in events:
#        ev = parse_event(raw)
#        if ev:
#            services[ev.service].append(ev)
#
#    alerts = []
#
#    for service, evts in services.items():
#        if len(evts) < 2:
#            continue
#
#        evts.sort(key=lambda e: e.timestamp)
#
#        for prev, curr in zip(evts, evts[1:]):
#            gap = curr.timestamp - prev.timestamp
#            if gap >= threshold_gap:
#
#                # first missed heartbeat is exactly one interval after prev.
#                first_missed = prev.timestamp + interval
#                alerts.append(
#                    {"service": service, "alerts_at": first_missed.strftime(ISO8601)}
#                )
#                break
#
#    return alerts


def detect_alerts(
    events: List[Dict[str, Any]], expected_interval_seconds: int, allowed_misses: int
) -> List[Dict[str, str]]:
    """
    Approach:
      - user a min heap per service instead of fully sorting lists.
      - pushing into heaps = O(log k_i) but summing across all services.
      - gives 0(N log S) when services << events;
      - Pop events in ascending timestamp order from each heap
    """

    interval = timedelta(seconds=expected_interval_seconds)
    threshold_gap = interval * (allowed_misses + 1)

    service_heaps = defaultdict(list)

    for raw in events:
        ev = parse_event(raw)
        if ev:
            # push (timestamp, event) so heap sorts by timestamp automatically
            heapq.heappush(service_heaps[ev.service], (ev.timestamp, ev))

    alerts = []

    for service, heap in service_heaps.items():
        if len(heap) < 2:
            continue  # cannot detect gaps with < 2 events

        # pop the earliest event
        _, prev_ev = heapq.heappop(heap)

        while heap:
            _, cur_ev = heapq.heappop(heap)

            gap = cur_ev.timestamp - prev_ev.timestamp

            if gap >= threshold_gap:
                # alert at the first missed heartbeat
                first_missed = prev_ev.timestamp + interval
                alerts.append(
                    {"service": service, "alert_at": first_missed.strftime(ISO8601)}
                )
                break  # only one alert per service

            prev_ev = cur_ev

    return alerts
