import os
from datetime import datetime

from Seleniumpractice.utils.config import Config  # run pytest from project root


def take_screenshot(driver, test_name, status="failed"):
    """
    Take a screenshot and save in screenshots/<status>/ folder
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Create folder if it doesn't exist
    screenshot_dir = os.path.join(Config.SCREENSHOT_PATH, status)
    os.makedirs(screenshot_dir, exist_ok=True)

    # Build file path
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")

    # Capture screenshot
    driver.save_screenshot(screenshot_path)

    return screenshot_path
