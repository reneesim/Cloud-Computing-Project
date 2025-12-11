import puppeteer from 'puppeteer';

const CONCURRENT_USERS = 100; // number of simultaneous tabs
const VISITS_PER_USER = 100;  // visits per tab
const URL = 'http://129.192.69.172:30080/';

async function singleUser(browser) {
  const page = await browser.newPage();
  for (let i = 0; i < VISITS_PER_USER; i++) {
    await page.goto(URL, { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 10));
  }
  await page.close();
}

async function runLoadTest() {
  const browser = await puppeteer.launch({ headless: true });

  const users = [];
  for (let i = 0; i < CONCURRENT_USERS; i++) {
    users.push(singleUser(browser));
  }

  await Promise.all(users);
  await browser.close();
  console.log('Load test finished');
}

runLoadTest();
