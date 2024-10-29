Run the application with `npm run start`.

# Example of telemetry Data

Telemetry data is collected locally, while the server is running, and stored in `data/telemetry.json`. Minor processing such as multiplication and averaging happens before the data is stored locally.</br>

When data collection has completed and the server is being shutdown with `Ctrl+C`, all data from the `telemetry.json` is sent to the MongoDB database. Timestamps from the stored data are reformatted from `Int64` to `BSON UTC Date Value` before being sent to MongoDB. Here are examples of telemetry data collected and stored:</br>

## Collected data (stored in local file)

```json
{
  "timestamp": 12949125000,
  "currentEngineRpm": 6312.5166015625,
  "speed": 24.725961685180664,
  "throttlePercent": 100,
  "brake": 0,
  "gear": 1,
  "steering": 0,
  "drivingLine": 49,
  "numWheelsOnRumbleStrip": 0,
  "grip": {
    "avgSlipRatio": 0.2009285787353292,
    "avgSlipAngle": 0.0003704243181346101,
    "avgCombinedSlip": 0.20811021188274026
  },
  "geometry": {
    "accelerationX": -0.013900518417358398,
    "accelerationY": -0.12439142167568207,
    "velocityX": 0.0006532669067382812,
    "velocityY": 0.007553219795227051
  },
  "currentLap": 1,
  "lapInfo": {
    "distanceTraveled": -0.2050597071647644,
    "segment": 0,
    "bestLapTime": 0,
    "lastLapTime": 0,
    "currentLapTime": 0.46666669845581055
  }
}
```

## Data stored in database

```json
{
  "_id": {
    "$oid": "67210dc2cb537e1d7ba02584"
  },
  "timestamp": {
    "$date": "1970-05-30T20:58:45.000Z"
  },
  "currentEngineRpm": 6312.5166015625,
  "speed": 24.725961685180664,
  "throttlePercent": 100,
  "brake": 0,
  "gear": 1,
  "steering": 0,
  "drivingLine": 49,
  "numWheelsOnRumbleStrip": 0,
  "currentLap": 1,
  "grip": {
    "avgSlipRatio": 0.2009285787353292,
    "avgSlipAngle": 0.0003704243181346101,
    "avgCombinedSlip": 0.20811021188274026,
    "_id": {
      "$oid": "67210dc2cb537e1d7ba02585"
    }
  },
  "geometry": {
    "accelerationX": -0.013900518417358398,
    "accelerationY": -0.12439142167568207,
    "velocityX": 0.0006532669067382812,
    "velocityY": 0.007553219795227051,
    "_id": {
      "$oid": "67210dc2cb537e1d7ba02586"
    }
  },
  "lapInfo": {
    "distanceTraveled": -0.2050597071647644,
    "segment": 0,
    "bestLapTime": 0,
    "lastLapTime": 0,
    "currentLapTime": 0.46666669845581055,
    "_id": {
      "$oid": "67210dc2cb537e1d7ba02587"
    }
  },
  "__v": 0
}
```
