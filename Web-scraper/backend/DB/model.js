import mongoose from "mongoose";

const dataSchema = new mongoose.Schema({
  title: String,
  link: String,
  createdAt: {
    type: Date,
    default: Date.now,
  }
});

export default mongoose.model("ScrapedData", dataSchema);
