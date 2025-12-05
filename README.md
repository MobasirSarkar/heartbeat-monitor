# Heartbeat Monitor

This project checks heartbeat events from different services and alerts when a service misses too many in a row.

## What “3 missed heartbeats” means

A service is expected to send a heartbeat at a fixed interval. If the time gap between two received heartbeats is large enough that three expected heartbeats should have occurred but did not, we treat that as “missing 3 heartbeats.”  
The alert time is the timestamp of the first heartbeat that should have arrived but didn’t.

## How unordered events are handled

Events may not arrive in time order. Before checking for missed heartbeats, the program groups events by service and sorts them by timestamp.

## How malformed events are handled

Malformed events are ignored. An event is considered malformed if it is missing a required field or has an invalid timestamp. Such events do not count as heartbeats.

## Setting up the environment

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate        (macOS / Linux)
.\.venv\Scripts\activate         (Windows)

Install dependencies:

pip install -r requirements.txt

## Running the program

python main.py or python3 main.py

## Running tests

pytest -v test.py
