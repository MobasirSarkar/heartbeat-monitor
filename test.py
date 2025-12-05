from heart_monitor import detect_alerts


def test_working_alert_case():
    events = [
        {"service": "email", "timestamp": "2025-08-04T10:00:00Z"},
        {"service": "email", "timestamp": "2025-08-04T10:01:00Z"},
        {"service": "email", "timestamp": "2025-08-04T10:02:00Z"},
        {"service": "email", "timestamp": "2025-08-04T10:06:00Z"},
    ]

    out = detect_alerts(events, expected_interval_seconds=60, allowed_misses=3)
    assert len(out) == 1
    assert out[0]["service"] == "email"
    assert out[0]["alert_at"] == "2025-08-04T10:03:00Z"


def test_near_miss_case():
    events = [
        {"service": "api", "timestamp": "2025-01-01T00:00:00Z"},
        {"service": "api", "timestamp": "2025-01-01T00:01:00Z"},
        {"service": "api", "timestamp": "2025-01-01T00:04:00Z"},
    ]
    out = detect_alerts(events, expected_interval_seconds=60, allowed_misses=3)
    assert out == []


def test_unordered_input():
    events = [
        {"service": "db", "timestamp": "2025-09-10T10:05:00Z"},
        {"service": "db", "timestamp": "2025-09-10T10:01:00Z"},
        {"service": "db", "timestamp": "2025-09-10T10:00:00Z"},
        {"service": "db", "timestamp": "2025-09-10T10:06:00Z"},
    ]

    out = detect_alerts(events, expected_interval_seconds=60, allowed_misses=3)
    assert len(out) == 1
    assert out[0]["alert_at"] == "2025-09-10T10:02:00Z"


def test_malformed_data():
    events = [
        {"service": "svc", "timestamp": "2025-01-01T00:00:00Z"},
        {"service": "svc"},  # missing timestamp
        {"timestamp": "2025-01-01T00:02:00Z"},  # missing service
        {"service": "svc", "timestamp": "INVALID"},  # invalid format
        {"service": "svc", "timestamp": "2025-01-01T00:06:00Z"},
    ]
    out = detect_alerts(events, expected_interval_seconds=60, allowed_misses=3)
    assert len(out) == 1
    assert out[0]["alert_at"] == "2025-01-01T00:01:00Z"
