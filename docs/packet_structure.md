# Overview

After being configured in-game, telemetry output sends data packets for use by external apps. This one-way UDP traffic is sent to a remote IP address at a rate of 60 packets per second. New to Forza Motorsport (2023), this functionality is now also available to the localhost address (127.0.01).

# Configuration

The following settings can be configured in-game and are found under SETTINGS > GAMEPLAY & HUD > “UDP RACE TELEMETRY” header:

- **Data Out:** Toggles the data output function on and off. When set to On, data will begin to send as soon as the player gets onto a track.
- **Data Out IP Address:** The target IP address of the remote machine receiving data. The localhost address (127.0.0.1) is supported.
- **Data Out IP Port:** The target IP port of the remote machine receiving data. Be sure your app is listening on the same port and that firewall rules allow data on these ports to be received by your app.
- **Data Out Packet Format:** The format of the data to send, either “Sled” or “Dash.” See below for an outline of each format.

# Output Structure

## Type notes:

[Letter][Number]</br>
The letter defines the type from one of the following:</br>
S Signed Integer</br>
U Unsigned Integer</br>
F Floating Point</br>
The number defines the amount of bits used.</br>

## Examples:

S8 is a signed byte with potential values between -128 and 127.</br>
F32 is a 32-bit floating point number, equivalent to float/single
</br>

## Dash (name of output structure)

<span style="color: #008000;">// = 1 when race is on. = 0 when in menus/race stopped …</span></br>
S32 IsRaceOn;</br>
</br>
<span style="color: #008000;">// Can overflow to 0 eventually</span></br>
U32 TimestampMS;</br>
F32 EngineMaxRpm;</br>
F32 EngineIdleRpm;</br>
F32 CurrentEngineRpm;</br>
</br>
<span style="color: #008000;">// In the car's local space; X = right, Y = up, Z = forward</span></br>
F32 AccelerationX;</br>
F32 AccelerationY;</br>
F32 AccelerationZ;</br>
</br>
<span style="color: #008000;">// In the car's local space; X = right, Y = up, Z = forward</span></br>
F32 VelocityX;</br>
F32 VelocityY;</br>
F32 VelocityZ;</br>
</br>
<span style="color: #008000;">// In the car's local space; X = pitch, Y = yaw, Z = roll</span></br>
F32 AngularVelocityX;</br>
F32 AngularVelocityY;</br>
F32 AngularVelocityZ;</br>
</br>
F32 Yaw;</br>
F32 Pitch;</br>
F32 Roll;</br>
</br>
<span style="color: #008000;">// Suspension travel normalized: 0.0f = max stretch; 1.0 = max compression</span></br>
F32 NormalizedSuspensionTravelFrontLeft;</br>
F32 NormalizedSuspensionTravelFrontRight;</br>
F32 NormalizedSuspensionTravelRearLeft;</br>
F32 NormalizedSuspensionTravelRearRight;</br>
</br>
<span style="color: #008000;">// Tire normalized slip ratio, = 0 means 100% grip and |ratio| &gt; 1.0 means loss of grip.</span></br>
F32 TireSlipRatioFrontLeft;</br>
F32 TireSlipRatioFrontRight;</br>
F32 TireSlipRatioRearLeft;</br>
F32 TireSlipRatioRearRight;</br>
</br>
<span style="color: #008000;">// Wheels rotation speed radians/sec.</span></br>
F32 WheelRotationSpeedFrontLeft;</br>
F32 WheelRotationSpeedFrontRight;</br>
F32 WheelRotationSpeedRearLeft;</br>
F32 WheelRotationSpeedRearRight;</br>
</br>
<span style="color: #008000;">// = 1 when wheel is on rumble strip, = 0 when off.</span></br>
S32 WheelOnRumbleStripFrontLeft;</br>
S32 WheelOnRumbleStripFrontRight;</br>
S32 WheelOnRumbleStripRearLeft;</br>
S32 heelOnRumbleStripRearRight;</br>
</br>
<span style="color: #008000;">// = from 0 to 1, where 1 is the deepest puddle</span></br>
F32 WheelInPuddleDepthFrontLeft;</br>
F32 WheelInPuddleDepthFrontRight;</br>
F32 WheelInPuddleDepthRearLeft;</br>
F32 WheelInPuddleDepthRearRight;</br>
</br>
<span style="color: #008000;">// Non-dimensional surface rumble values passed to controller force feedback</span></br>
F32 SurfaceRumbleFrontLeft;</br>
F32 SurfaceRumbleFrontRight;</br>
F32 SurfaceRumbleRearLeft;</br>
F32 SurfaceRumbleRearRight;</br>
</br>
<span style="color: #008000;">// Tire normalized slip angle, = 0 means 100% grip and |angle| &gt; 1.0 means loss of grip.</span></br>
F32 TireSlipAngleFrontLeft;</br>
F32 TireSlipAngleFrontRight;</br>
F32 TireSlipAngleRearLeft;</br>
F32 TireSlipAngleRearRight;</br>
</br>
<span style="color: #008000;">// Tire normalized combined slip, = 0 means 100% grip and |slip| &gt; 1.0 means loss of grip.</span></br>
F32 TireCombinedSlipFrontLeft;</br>
F32 TireCombinedSlipFrontRight;</br>
F32 TireCombinedSlipRearLeft;</br>
F32 TireCombinedSlipRearRight;</br>
</br>
<span style="color: #008000;">// Actual suspension travel in meters</span></br>
F32 SuspensionTravelMetersFrontLeft;</br>
F32 SuspensionTravelMetersFrontRight;</br>
F32 SuspensionTravelMetersRearLeft;</br>
F32 SuspensionTravelMetersRearRight;</br>
</br>
<span style="color: #008000;">// Unique ID of the car make/model</span></br>
S32 CarOrdinal;</br>
</br>
<span style="color: #008000;">// Between 0 (D -- worst cars) and 7 (X class -- best cars) inclusive</span></br>
S32 CarClass;</br>
</br>
<span style="color: #008000;">// Between 100 (worst car) and 999 (best car) inclusive</span></br>
S32 CarPerformanceIndex;</br>
</br>
<span style="color: #008000;">// 0 = FWD, 1 = RWD, 2 = AWD</span></br>
S32 DrivetrainType;</br>
</br>
<span style="color: #008000;">// Number of cylinders in the engine</span></br>
S32 NumCylinders;</br>
F32 PositionX;</br>
F32 PositionY;</br>
F32 PositionZ;</br>
F32 Speed;</br>
F32 Power;</br>
F32 Torque;</br>
F32 TireTempFrontLeft;</br>
F32 TireTempFrontRight;</br>
F32 TireTempRearLeft;</br>
F32 TireTempRearRight;</br>
F32 Boost;</br>
F32 Fuel;</br>
F32 DistanceTraveled;</br>
F32 BestLap;</br>
F32 LastLap;</br>
F32 CurrentLap;</br>
F32 CurrentRaceTime;</br>
U16 LapNumber;</br>
U8 RacePosition;</br>
U8 Accel;</br>
U8 Brake;</br>
U8 Clutch;</br>
U8 HandBrake;</br>
U8 Gear;</br>
S8 Steer;</br>
S8 NormalizedDrivingLine;</br>
S8 NormalizedAIBrakeDifference;</br>
</br>
F32 TireWearFrontLeft;</br>
F32 TireWearFrontRight;</br>
F32 TireWearRearLeft;</br>
F32 TireWearRearRight;</br>
</br>
<span style="color: #008000;">// ID for track</span></br>
S32 TrackOrdinal;</div>
