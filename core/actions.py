import logging
from utils.screenshot import take_screenshot


def fill_action(page, locator, value, element_desc, screenshot_dir, goal, idx):
    page.fill(locator, value)
    logging.info(f"Entered '{value}' in {element_desc} using locator '{locator}'")
    take_screenshot(page, f"enter_{element_desc}", screenshot_dir, goal, idx)

def click_action(page, locator, element_desc, screenshot_dir, goal, idx):
    page.click(locator)
    logging.info(f"Clicked on {element_desc} using locator '{locator}'")
    take_screenshot(page, f"click_{element_desc}", screenshot_dir, goal, idx)

def verify_action(page, locator, element_desc, screenshot_dir, goal, idx):
    if page.is_visible(locator):
        logging.info(f"Verified {element_desc} is displayed using locator '{locator}'")
        take_screenshot(page, f"verify_{element_desc}", screenshot_dir, goal, idx)
    else:
        raise Exception(f"{element_desc} not displayed") 