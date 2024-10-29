// models/User.js
import mongoose from "mongoose";

const GripSchema = new mongoose.Schema({
  avgSlipRatio: Number,
  avgSlipAngle: Number,
  avgCombinedSlip: Number,
});

const GeometrySchema = new mongoose.Schema({
  accelerationX: Number,
  accelerationY: Number,
  velocityX: Number,
  velocityY: Number,
});

const LapInfoSchema = new mongoose.Schema({
  distanceTraveled: Number,
  segment: Number,
  bestLapTime: Number,
  lastLapTime: Number,
  currentLapTime: Number,
});

const TelemetrySchema = new mongoose.Schema(
  {
    timestamp: Date,
    currentEngineRpm: Number,
    speed: Number,
    throttlePercent: Number,
    brake: Number,
    gear: Number,
    steering: Number,
    drivingLine: Number,
    numWheelsOnRumbleStrip: Number,
    currentLap: Number,
    grip: GripSchema,
    geometry: GeometrySchema,
    lapInfo: LapInfoSchema,
  },
  { strict: false }
);

export const Telemetry = mongoose.model("Telemetry", TelemetrySchema);
