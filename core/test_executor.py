import time
import logging
from core.actions import fill_action, click_action, verify_action
from utils.screenshot import take_screenshot

def try_locator_with_retry(element_desc, page, locator_manager, action_fn, screenshot_dir, goal, idx, value=None, fail_prefix=None):
    retries = 3
    for attempt in range(retries):
        locator = locator_manager.get_locator(element_desc, page.content(), save_cache=True)
        if locator:
            try:
                page.wait_for_selector(locator, timeout=10000)
                if value is not None:
                    action_fn(page, locator, value, element_desc, screenshot_dir, goal, idx)
                else:
                    action_fn(page, locator, element_desc, screenshot_dir, goal, idx)
                return True
            except Exception as e:
                logging.warning(f"Attempt {attempt+1}: Failed to use locator '{locator}' for '{element_desc}': {e}")
                take_screenshot(page, f"{fail_prefix or 'fail'}_{element_desc}_attempt{attempt+1}", screenshot_dir, goal, idx)
                # Remove the bad locator from cache and try again
                if element_desc in locator_manager.cache:
                    del locator_manager.cache[element_desc]
                    locator_manager.save_cache()
        else:
            logging.error(f"Attempt {attempt+1}: Locator not found for {element_desc}")
            take_screenshot(page, f"{fail_prefix or 'fail'}_{element_desc}_attempt{attempt+1}", screenshot_dir, goal, idx)
    return False

def execute_test_case(test_case, page, locator_manager, screenshot_dir):
    goal = test_case.get("goal", "No goal specified")
    actions = test_case.get("action", "").split(". ")
    logging.info(f"Executing test case: {goal}")
    for idx, action in enumerate(actions):
        action = action.strip()
        if not action:
            continue
        try:
            if action.startswith("Open the"):
                url = action.replace("Open the ", "").strip()
                page.goto(url)
                logging.info(f"Opened URL: {url}")
                take_screenshot(page, "open_url", screenshot_dir, goal, idx)
            elif action.startswith("Enter"):
                parts = action.split(" in ")
                value = parts[0].replace("Enter ", "").strip()
                element_desc = parts[1].strip()
                success = try_locator_with_retry(element_desc, page, locator_manager, fill_action, screenshot_dir, goal, idx, value=value, fail_prefix="fail_enter")
                if not success:
                    return False
            elif action.startswith("Wait for"):
                seconds = float(action.replace("Wait for ", "").replace(" seconds", "").strip())
                time.sleep(seconds)
                logging.info(f"Waited for {seconds} seconds")
                take_screenshot(page, "wait", screenshot_dir, goal, idx)
            elif action.startswith("Click on"):
                element_desc = action.replace("Click on the ", "").strip()
                success = try_locator_with_retry(element_desc, page, locator_manager, click_action, screenshot_dir, goal, idx, fail_prefix="fail_click")
                if not success:
                    return False
            elif action.startswith("Verify"):
                element_desc = action.replace("Verify the Dashboard Page, ", "").strip()
                success = try_locator_with_retry(element_desc, page, locator_manager, verify_action, screenshot_dir, goal, idx, fail_prefix="fail_verify")
                if not success:
                    return False
            elif action.startswith("In valid Login credentials message"):
                element_desc = "Invalid Login credentials message"
                success = try_locator_with_retry(element_desc, page, locator_manager, verify_action, screenshot_dir, goal, idx, fail_prefix="fail_invalid_login_message")
                if not success:
                    return False
            elif action == "Close the browser":
                page.context.close()
                logging.info("Browser closed")
                take_screenshot(page, "close_browser", screenshot_dir, goal, idx)
                return True
        except Exception as e:
            logging.error(f"Error executing action '{action}': {str(e)}")
            take_screenshot(page, f"error_{action}", screenshot_dir, goal, idx)
            return False
    return True 