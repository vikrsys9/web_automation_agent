import os
from playwright.sync_api import Error as PlaywrightError
import logging

def take_screenshot(page, step_name, screenshot_dir, test_goal, step_idx):
    safe_goal = ''.join(c for c in test_goal if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
    filename = f"{safe_goal}_step{step_idx}_{step_name}.png"
    filepath = os.path.join(screenshot_dir, filename)
    try:
        page.screenshot(path=filepath, full_page=True)
        logging.info(f"Screenshot saved: {filepath}")
    except PlaywrightError as e:
        logging.warning(f"Could not take screenshot at {step_name}: {e}")
    return filepath 