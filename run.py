from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from zipsolver.algorithm.search import Search
from zipsolver.screen_interactive.web_interactor import draw_path, scrape_puzzle

ZIP_PATH = "https://www.linkedin.com/games/zip/"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(ZIP_PATH)
        page.get_by_text("Start game").click()

        try:
            puzzle, board_data = scrape_puzzle(page)
        except PlaywrightTimeoutError:
            browser.close()
            raise

        result = Search(puzzle).find_path()

        if result is None:
            print("No solution found")
        else:
            print("Solution path:", result)
            draw_path(page, board_data, result)

        input("Press Enter to close the browser...")
        browser.close()


if __name__ == "__main__":
    main()
