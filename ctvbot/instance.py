import threading
import time
from playwright.sync_api import sync_playwright

class Instance(threading.Thread):
    def __init__(
        self,
        user_agent,
        proxy_dict,
        target_url,
        status_report_callback,
        location_info=None,
        headless=True,
        auto_restart=False,
        instance_id=None,
    ):
        threading.Thread.__init__(self)
        self.id = instance_id
        self.user_agent = user_agent
        self.proxy_dict = proxy_dict
        self.target_url = target_url
        self.status_report_callback = status_report_callback
        self.location_info = location_info
        self.headless = headless
        self.auto_restart = auto_restart

        self.status = "alive"
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def run(self):
        self.status = "starting"
        logger.info(f"Instance {self.id} starting")

        self.spawn_page()

        if self.status == "dead":
            return

        self.todo_after_spawn()

        if self.status == "dead":
            return

        self.loop_and_check()

    def restart(self):
        self.status = "restart"

    def stop(self):
        self.status = "stopped"
        logger.info(f"Instance {self.id} stopped")

    def clean_up_playwright(self):
        if self.page:
            self.page.close()
            self.page = None

        if self.context:
            self.context.close()
            self.context = None

        if self.browser:
            self.browser.close()
            self.browser = None

        if self.playwright:
            self.playwright.stop()
            self.playwright = None

    def __del__(self):
        self.clean_up_playwright()

    def log_status(self, status):
        logger.info(f"Instance {self.id} status: {status}")
        self.status_report_callback(self.id, status)

    def on_page_crash(self):
        self.log_status("crashed")

        if self.auto_restart:
            self.restart()

    def on_page_close(self):
        self.log_status("closed")

        if self.auto_restart:
            self.restart()

    def on_page_error(self, message):
        self.log_status("error")
        logger.error(
            f"Encountered error {message} while running. Instance will restart automatically"
        )

        self.clean_up_playwright()

        if self.auto_restart:
            self.status = "restarting"
            logger.info("Restarting")
            self.start()

    def loop_and_check(self):
        while True:
            if self.status == "restart":
                break

            if self.status == "dead":
                self.status = "restarting"
                logger.info("Restarting")
                break

            self.check_is_alive()
            time.sleep(10)

    def check_is_alive(self):
        if not self.page or self.status != "alive":
            return

        try:
            self.page.goto(self.target_url, timeout=60000)
        except Exception as e:
            message = e.args[0][:25] if e.args else ""
            logger.error(f"{self.id}: Error loading page: {message}")
            self.status = "dead"

    def spawn_page(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.webkit.launch(headless=self.headless)

        if self.headless:
            self.context = self.browser.new_context(
                user_agent=self.user_agent, proxy=self.proxy_dict
            )
        else:
            self.context = self.browser.new_context(user_agent=self.user_agent)

        self.page = self.context.new_page()
        self.page.on("crash", lambda: self.on_page_crash())
        self.page.on("close", lambda: self.on_page_close())
        self.page.on("pageerror", lambda: self.on_page_error())

    def todo_after_spawn(self):
        # Implemente suas ações personalizadas aqui, como fazer login, navegar em páginas, etc.
        # Lembre-se de adicionar tratamento de erros adequado para lidar com exceções
        raise NotImplementedError("todo_after_spawn method must be overridden")
