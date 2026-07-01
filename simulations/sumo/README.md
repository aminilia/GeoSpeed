# SUMO Simulation Support

SUMO is optional and not required for the default GeoSpeed Auto FDE quick start.

This folder documents how future SUMO trajectory outputs could be converted into the vehicle signal replay contract used by `vehicle-signals-python`.

Suggested flow:

1. Export SUMO floating-car or trip trajectory output.
2. Convert timestamp, position, heading, speed, and route ID.
3. Join matched road segment and speed-limit metadata from GeoSpeed sample data.
4. Emit replay JSON compatible with `POST /signals/replay` or scenario files.

