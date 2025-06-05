import os
import shutil
import json
from playwright.sync_api import sync_playwright
import google.generativeai as genai
from config.config_loader import load_config
from utils.logger import setup_logger
from utils.token_counter import TokenCounter
from core.locator import LocatorManager
from core.test_executor import execute_test_case
from core.report import generate_html_report



def main():
    # Setup logger
    logger = setup_logger()
    # Load config
    config = load_config()
    screenshot_dir = config.get('screenshot_dir', 'web_automation_agent/screenshots')
    if os.path.exists(screenshot_dir):
        shutil.rmtree(screenshot_dir)
    os.makedirs(screenshot_dir, exist_ok=True)
    # Mobile emulation
    mobile_conf = config.get('mobile', {})
    is_mobile = mobile_conf.get('enabled', False)
    device = mobile_conf.get('device', 'iPhone 12')
    # Load test cases
    with open('test_case.json', 'r') as f:
        test_cases = json.load(f)
    # Gemini API setup
    os.environ['GEMINI_API_KEY'] = 'GEMINI_API_KEY'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    # Locator manager and token counter
    locator_cache_file = 'data/locator_cache.json'
    token_counter = TokenCounter()
    locator_manager = LocatorManager(locator_cache_file, model, token_counter)
    # Playwright
    results = []
    with sync_playwright() as p:
        browser_type = config.get('browser', 'chromium')
        headless = config.get('headless', False)
        if is_mobile:
            device_dict = p.devices.get(device, p.devices['iPhone 12'])
            context = getattr(p, browser_type).launch(headless=headless).new_context(**device_dict)
        else:
            viewport = config.get('viewport', {'width': 1280, 'height': 720})
            context = getattr(p, browser_type).launch(headless=headless).new_context(viewport=viewport)
        page = context.new_page()
        for test_case in test_cases:
            before = set(os.listdir(screenshot_dir))
            success = execute_test_case(test_case, page, locator_manager, screenshot_dir)
            after = set(os.listdir(screenshot_dir))
            new_shots = sorted(list(after - before))
            new_shots = [os.path.join(screenshot_dir, s) for s in new_shots]
            results.append({
                'goal': test_case['goal'],
                'success': success,
                'screenshots': new_shots
            })
        context.close()
    locator_manager.save_cache()
    report_path = config.get('report_path', 'reports/automation_report.html')
    generate_html_report(results, report_path)
    print(f"Total Gemini API tokens consumed: {token_counter.get_total()}")

if __name__ == "__main__":
    main() 