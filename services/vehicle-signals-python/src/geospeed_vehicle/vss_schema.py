from __future__ import annotations

VSS_SIGNALS: dict[str, str] = {
    "Vehicle.Speed": "Current vehicle speed in miles per hour for this simulator.",
    "Vehicle.CurrentLocation.Latitude": "Current WGS84 latitude.",
    "Vehicle.CurrentLocation.Longitude": "Current WGS84 longitude.",
    "Vehicle.Heading": "Current vehicle heading in degrees.",
    "Vehicle.ADAS.CruiseControl.SpeedSet": "Cruise-control set speed.",
    "Vehicle.ADAS.CruiseControl.IsActive": "Cruise-control active state.",
    "Vehicle.ADAS.SpeedLimitAssist.IsActive": "Speed-limit assist active state.",
    "Vehicle.Cabin.Infotainment.Navigation.ActiveRouteId": "Active navigation route id.",
    "Vehicle.Powertrain.Transmission.CurrentGear": "Current transmission gear.",
}

