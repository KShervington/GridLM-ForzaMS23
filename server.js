import { createSocket } from "dgram";
import { createWriteStream } from "fs";
import { connectToDb, sendDataToDb } from "./src/config/db.js";

// Create a UDP socket
const server = createSocket("udp4");

// Define the file where the parsed data will be saved
const filePath = "data/telemetry.json";
const writeStream = createWriteStream(filePath);

const trackLength = 2253;
const numSegments = 10;
let sep = ""; // separator for json data

// Returns the distance traveled in the current lap
function getLapDistance(totalDistance, currentLap) {
  return totalDistance - currentLap * trackLength;
}

// Calculate the current segment of the lap based on number of segments and track length
function getCurrentSegment(currDistance) {
  const distancePerSeg = trackLength / numSegments;

  return Math.floor(currDistance / distancePerSeg) + 1;
}

// Function to parse the binary data according to the Dash format
function parseDashPacket(msg) {
  const parsedData = {};

  let isDriving = false;

  // Create a buffer from the message; contains all data from the received packet
  const buffer = Buffer.from(msg);

  isDriving = Number(buffer.readInt32LE(0)) === 1 ? true : false;

  if (isDriving) {
    parsedData.timestamp = buffer.readUInt32LE(4) * 1000; // convert to 64-bit integer by multiplying by 1000
    parsedData.currentEngineRpm = buffer.readFloatLE(16);
    parsedData.speed = buffer.readFloatLE(244);
    parsedData.throttlePercent = Math.floor(buffer.readUInt8(303) / 255) * 100; // 0 - 255 for how much throttle is being applied
    parsedData.brake = buffer.readUInt8(304);
    parsedData.gear = buffer.readUInt8(307);
    parsedData.steering = buffer.readInt8(308); // 127 is full right; -127 is full left; up and down are both 0
    parsedData.drivingLine = buffer.readInt8(309); // not sure how to interpret this value

    parsedData.numWheelsOnRumbleStrip = parseInt(
      buffer.readFloatLE(116) +
        buffer.readFloatLE(120) +
        buffer.readFloatLE(124) +
        buffer.readFloatLE(128)
    );

    parsedData.grip = {}; // values greater than 1 indicate loss of grip
    parsedData.grip.avgSlipRatio = Math.abs(
      (buffer.readFloatLE(84) +
        buffer.readFloatLE(88) +
        buffer.readFloatLE(92) +
        buffer.readFloatLE(96)) /
        4
    );

    parsedData.grip.avgSlipAngle = Math.abs(
      (buffer.readFloatLE(164) +
        buffer.readFloatLE(168) +
        buffer.readFloatLE(172) +
        buffer.readFloatLE(176)) /
        4
    );

    parsedData.grip.avgCombinedSlip = Math.abs(
      (buffer.readFloatLE(180) +
        buffer.readFloatLE(184) +
        buffer.readFloatLE(188) +
        buffer.readFloatLE(192)) /
        4
    );

    parsedData.geometry = {};
    parsedData.geometry.accelerationX = buffer.readFloatLE(20);
    parsedData.geometry.accelerationY = buffer.readFloatLE(24);
    parsedData.geometry.velocityX = buffer.readFloatLE(32);
    parsedData.geometry.velocityY = buffer.readFloatLE(36);

    parsedData.currentLap = buffer.readUInt16LE(300) + 1; // 1st lap is considered lap 0

    parsedData.lapInfo = {};
    // Distance is cumulative so it needs to be adjusted
    parsedData.lapInfo.distanceTraveled = getLapDistance(
      buffer.readFloatLE(280),
      parsedData.currentLap - 1
    );

    parsedData.lapInfo.segment = getCurrentSegment(
      parsedData.lapInfo.distanceTraveled
    );

    parsedData.lapInfo.bestLapTime = buffer.readFloatLE(284);
    parsedData.lapInfo.lastLapTime = buffer.readFloatLE(288);
    parsedData.lapInfo.currentLapTime = buffer.readFloatLE(292);
  }

  return parsedData;
}

server.on("listening", () => {
  console.log("UDP server listening on 127.0.0.1:3000");
  writeStream.write("[");
});

// When a message is received
server.on("message", (msg, rinfo) => {
  // Parse the received data
  const parsedData = parseDashPacket(msg);

  if (Object.keys(parsedData).length > 0) {
    writeStream.write(sep + JSON.stringify(parsedData, null, 4));

    // If there is no separator, which is the default, then assign one
    if (!sep) sep = ",\n";
  }
});

// Handle errors
server.on("error", (err) => {
  console.error(`Server error:\n${err.stack}`);
  server.disconnect();
});

// Bind to the port and IP where Forza is sending data
server.bind(3000, "127.0.0.1", () => {
  connectToDb();
});

// Tasks to perform before server is shutdown
const shutdownOperations = async function () {
  // Write to end of file to create valid json array
  writeStream.write("]");
  await new Promise((resolve) => writeStream.end(resolve));
  console.log("File writing completed, sending data to DB.");

  // Send database from file to database
  await sendDataToDb();
};

// Handle SIGINT signal (Ctrl+C)
process.on("SIGINT", () => {
  console.log("Received SIGINT, initiating server shutdown...");

  // Close the server
  server.close(async () => {
    console.log("Performing shutdown operations...");

    await shutdownOperations();

    console.log("Shutdown operations complete.\n\nSHUTTING DOWN SERVER");
    process.exit(0); // Exit the process
  });
});
