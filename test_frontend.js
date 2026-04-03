const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage({
        viewport: { width: 375, height: 667 } // Mobile viewport
    });

    // Go to index page
    await page.goto('http://localhost:8000/index.html');

    // Wait for preloader to disappear
    await page.waitForTimeout(1000);

    await page.screenshot({ path: 'mobile_index.png', fullPage: true });

    // Open mobile menu
    await page.click('#mobile-menu-btn');
    await page.waitForTimeout(500); // Wait for transition
    await page.screenshot({ path: 'mobile_menu_open.png' });

    await browser.close();
    console.log("Screenshots captured");
})();
