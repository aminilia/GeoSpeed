import { chromium } from "playwright";
import path from "path";
import fs from "fs";

const appUrl = "http://localhost:5173/";
const assetsDir = path.resolve("../../docs/assets");

async function ensureAssetsDir() {
  if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
  }
}

async function capturePage(page: any, filename: string) {
  await page.waitForTimeout(800);
  await page.screenshot({
    path: path.join(assetsDir, filename),
    fullPage: true
  });
}

async function clickIfVisible(page: any, label: RegExp) {
  const item = page.getByText(label);
  if (await item.count()) {
    await item.first().click();
    await page.waitForTimeout(800);
    return true;
  }
  return false;
}

async function main() {
  await ensureAssetsDir();

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 }
  });

  await page.goto(appUrl, {
    waitUntil: "networkidle"
  });

  // 1. Main dashboard
  await capturePage(page, "dashboard-overview.png");

  // 2. Partner Issue Triage
  await clickIfVisible(page, /partner issue triage|partner issues|issues/i);
  await capturePage(page, "partner-issue-triage.png");

  await browser.close();

  console.log("Screenshots saved to docs/assets/");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});