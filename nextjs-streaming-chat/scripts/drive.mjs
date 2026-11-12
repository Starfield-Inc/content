// Drive the real page in Chrome, the way a person would, and save screenshots.
// usage: node scripts/drive.mjs chat | stop | error
import puppeteer from "puppeteer-core";
import { mkdirSync } from "node:fs";

const CHROME = process.env.CHROME_BIN ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const scenario = process.argv[2];
mkdirSync("evidence", { recursive: true });
mkdirSync("images", { recursive: true });

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 760, height: 820, deviceScaleFactor: 2 });
await page.goto("http://127.0.0.1:8129/", { waitUntil: "networkidle0" });

const t0 = Date.now();
const ms = () => `${Date.now() - t0} ms`;
const shot = async (name) => {
  await page.screenshot({ path: `evidence/shot-${name}.png` });
  await page.screenshot({ path: `images/shot-${name}.png` });
  console.log(`saved screenshot ${name}`);
};
const ask = async (text) => {
  await page.type("#input", text);
  await page.click("#send");
};
const lastAnswer = () =>
  page.$$eval(".msg.assistant p", (ps) => (ps.length ? ps[ps.length - 1].textContent : ""));
const sleep = (n) => new Promise((r) => setTimeout(r, n));

try {
  if (scenario === "chat") {
    await ask("Give me three tips for a hackathon demo, one line each.");
    await page.waitForFunction(() => document.querySelector("#stop") && (document.querySelector(".msg.assistant p")?.textContent.length ?? 0) > 25, { timeout: 30000 });
    console.log(`at ${ms()}: Stop button visible, answer so far: ${JSON.stringify(await lastAnswer())}`);
    await shot("streaming");
    await page.waitForSelector("#send", { timeout: 60000 });
    console.log(`at ${ms()}: answer finished, ${(await lastAnswer()).length} characters`);
    await ask("Which of those three is quickest to do in ten minutes?");
    await page.waitForSelector("#stop", { timeout: 30000 });
    await page.waitForSelector("#send", { timeout: 60000 });
    const count = await page.$$eval(".msg", (m) => m.length);
    console.log(`at ${ms()}: second answer finished`);
    console.log(`messages on page: ${count}`);
    console.log(`second answer: ${JSON.stringify(await lastAnswer())}`);
    await shot("history");
  } else if (scenario === "stop") {
    await ask("Write a story of about 250 words about a robot at a hackathon.");
    await page.waitForFunction(() => (document.querySelector(".msg.assistant p")?.textContent.length ?? 0) > 60, { timeout: 30000 });
    await page.click("#stop");
    await page.waitForSelector("#send", { timeout: 10000 });
    const atStop = (await lastAnswer()).length;
    console.log(`clicked Stop: ${atStop} characters on screen, Send button is back`);
    await sleep(2500);
    const later = (await lastAnswer()).length;
    console.log(`2.5 seconds later: ${later} characters (${later === atStop ? "no more text arrived" : "text kept arriving"})`);
    console.log(`marked as stopped: ${(await page.$$eval(".tag", (t) => t.length)) === 1}`);
    await shot("stopped");
    await sleep(500);
  } else if (scenario === "error") {
    await ask("Hello");
    await page.waitForSelector("#error", { timeout: 30000 });
    console.log(`error shown: ${JSON.stringify(await page.$eval("#error span", (e) => e.textContent))}`);
    console.log(`Try again button present: ${(await page.$("#retry")) !== null}`);
    console.log(`you can still type: ${await page.$eval("#input", (i) => !i.disabled)}`);
    await shot(process.argv[3] ?? "error");
  } else {
    throw new Error(`unknown scenario ${scenario}`);
  }
} catch (err) {
  console.log(`FAILED at ${ms()}: ${err.message}`);
  await shot(`failed-${scenario}`).catch(() => {});
  process.exitCode = 1;
} finally {
  await browser.close();
}
