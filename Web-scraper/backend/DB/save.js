import "./connect.js";
import ScrapedData from "./model.js";

export const saveToDB = async (title, link) => {
  try {
    await ScrapedData.create({ title, link });
    console.log("Saved to DB");
  } catch (err) {
    console.log(err);
  }
};

async function saveData() {
  await saveToDB("Example Title", "https://example.com");
}

saveData();
