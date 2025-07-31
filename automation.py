from playwright.sync_api import sync_playwright

class LinkedInBot:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.browser = None
        self.page = None
        self.context = None

    def login(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("https://www.linkedin.com/login")
        self.page.fill("input#username", self.email)
        self.page.fill("input#password", self.password)
        self.page.click("button[type='submit']")
        # Wait for either the jobs search input or an error message
        try:
            self.page.wait_for_selector("input[placeholder='Search jobs']", timeout=15000)
        except Exception:
            self.page.screenshot(path="debug_after_login.png")
            if self.page.query_selector("div[role='alert']"):
                raise Exception("Login failed: Check your credentials or for a captcha.")
            else:
                raise Exception("Login may have failed or a captcha is present. See debug_after_login.png.")

    def search_jobs(self, keywords: str, location: str):
        self.page.goto("https://www.linkedin.com/jobs/")
        self.page.wait_for_selector("input[placeholder='Search jobs']")
        self.page.fill("input[placeholder='Search jobs']", keywords)
        self.page.fill("input[placeholder='Search location']", location)
        self.page.click("button[aria-label='Search']")
        self.page.wait_for_load_state("networkidle")

    def get_job_descriptions(self):
        job_descriptions = []
        self.page.wait_for_selector(".jobs-search-results__list-item")
        job_cards = self.page.query_selector_all(".jobs-search-results__list-item")[:5]
        for card in job_cards:
            card.click()
            self.page.wait_for_selector(".jobs-description-content__text")
            desc = self.page.query_selector(".jobs-description-content__text")
            if desc:
                job_descriptions.append(desc.inner_text())
        return job_descriptions

    def close(self):
        if self.browser:
            self.browser.close()