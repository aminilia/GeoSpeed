# Vehicle Signal Model

## VSS-Style Signals Used

- `Vehicle.Speed`
- `Vehicle.CurrentLocation.Latitude`
- `Vehicle.CurrentLocation.Longitude`
- `Vehicle.Heading`
- `Vehicle.ADAS.CruiseControl.SpeedSet`
- `Vehicle.ADAS.CruiseControl.IsActive`
- `Vehicle.ADAS.SpeedLimitAssist.IsActive`
- `Vehicle.Cabin.Infotainment.Navigation.ActiveRouteId`
- `Vehicle.Powertrain.Transmission.CurrentGear`

## Scenario Replay Model

Each replay point includes timestamp, position, heading, vehicle speed, matched road segment, speed limit, alert status, and ADAS mismatch flag.

## Validation Logic

The simulator raises mismatch flags when cruise-control set speed exceeds the speed limit while speed-limit assist is active.

## Limitations

Signals are synthetic and intended for integration design, not vehicle certification.

