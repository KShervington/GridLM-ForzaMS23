import mongoose from "mongoose";
import dotenv from "dotenv";
import { Telemetry } from "../models/Telemetry.js";
import { readFileSync } from "fs";

dotenv.config();
mongoose.set("debug", false); // Logs database operations when true

export const connectToDb = async function () {
  let uri = "";

  let clientOptions = {
    serverApi: { version: "1", strict: false, deprecationErrors: true },
  };

  if (process.env.ENVIRONMENT === "prod") {
    uri = process.env.MONGODB_CONNECTION_URI;
    clientOptions.dbName = "SuzukaCircuit";
  } else {
    uri = process.env.MONGODB_LOCAL_CONNECTION_URI;
  }

  try {
    // Create a Mongoose client with a MongoClientOptions object to set the Stable API version
    await mongoose.connect(uri, clientOptions);

    await mongoose.connection.db.admin().command({ ping: 1 });

    console.log("Successfully connected to database!");
  } catch (err) {
    console.dir(err);
  }
};

export const sendDataToDb = async function () {
  try {
    const dataPath = "./data/telemetry.json";
    const jsonData = JSON.parse(readFileSync(dataPath, "utf-8"));

    // Convert timestamp field to Date object and insert into MongoDB
    const formattedJson = jsonData.map((object) => ({
      ...object,
      timestamp: new Date(object.timestamp), // Convert string to Date
    }));

    // Insert data into MongoDB
    await Telemetry.insertMany(formattedJson)
      .then(() => console.log("Data sent successfully!"))
      .catch((error) => {
        console.error("Error inserting into database:\n", err.message);
      });
  } catch (err) {
    console.error("Error sending data:", err.message);
  } finally {
    // Close connection
    mongoose.connection.close();

    console.log("Disconnected from DB");
  }
};
