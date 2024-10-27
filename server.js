const dgram = require("dgram");
const fs = require("fs");
const path = require("path");

// Create a UDP socket
const server = dgram.createSocket("udp4");

// Define the file where the parsed data will be saved
const filePath = path.join(__dirname, "parsed_output.json");
const writeStream = fs.createWriteStream(filePath);

// Function to parse the binary data according to the Sled format
function parseDashPacket(msg) {
  const parsedData = {};

  let isDriving = false;

  // Create a buffer from the message
  const buffer = Buffer.from(msg);

  // Parse each part of the packet (example using the Sled format)
  parsedData.isRaceOn = buffer.readInt32LE(0);

  isDriving = parsedData.isRaceOn === 1 ? true : false;

  if (isDriving) {
    parsedData.timestamp = buffer.readUInt32LE(4);
    parsedData.currentEngineRpm = buffer.readFloatLE(16);
    parsedData.accelerationX = buffer.readFloatLE(20);
    parsedData.accelerationY = buffer.readFloatLE(24);
    parsedData.accelerationZ = buffer.readFloatLE(28);
    parsedData.velocityX = buffer.readFloatLE(32);
    parsedData.velocityY = buffer.readFloatLE(36);
    parsedData.velocityZ = buffer.readFloatLE(40);
  }

  return parsedData;
}

// When a message is received
server.on("message", (msg, rinfo) => {
  console.log(`.`);

  // Parse the received data
  const parsedData = parseDashPacket(msg);

  // Write parsed data to file
  writeStream.write(JSON.stringify(parsedData) + ",\n");
});

// Handle errors
server.on("error", (err) => {
  console.error(`Server error:\n${err.stack}`);
  server.close();
});

// Bind to the port and IP where Forza is sending data
server.bind(3000, "127.0.0.1", () => {
  console.log("UDP server listening on 127.0.0.1:3000");
});
