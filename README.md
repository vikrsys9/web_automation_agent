# Web Automation Agent

## Overview
This project is a web automation framework that leverages Playwright and Gemini LLM to automate browser actions, generate reports, and provide a web-based configuration editor. It supports mobile emulation, self-healing locators, and visual reporting.

## Features
- Web UI for editing automation config and test cases
- Automated browser actions using Playwright
- Locator generation and self-healing using Gemini LLM
- Screenshot capture and HTML report generation
- Mobile device emulation
- REST API for config and test case management

## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies
- Playwright browsers (see below)

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

## Configuration
- `automation_config.json`: Main configuration file (browser, headless, screenshot dir, retries, timeouts, mobile emulation, etc.)
- `test_case.json`: List of test cases with `goal` and `action` fields
- `data/locator_cache.json`: Cache for element locators

## Running the Project
### 1. Run the Web Server (for config editor)
```bash
python server.py
```
- Visit [http://localhost:5000](http://localhost:5000) to access the config editor UI.

### 2. Run Automation Directly
```bash
python main.py
```
- This will execute the test cases and generate a report in the `reports/` directory.

## File Structure
```
.
├── main.py                  # Main automation runner
├── server.py                # Flask server for web UI/API
├── config_editor.html       # Web UI for config/test case editing
├── automation_config.json   # Automation configuration
├── test_case.json           # Test cases
├── data/
│   └── locator_cache.json   # Locator cache
├── core/
│   ├── locator.py           # Locator manager (LLM + self-healing)
│   ├── report.py            # HTML report generator
│   ├── test_executor.py     # Test case executor
│   └── actions.py           # Action implementations
├── utils/
│   ├── screenshot.py        # Screenshot utility
│   ├── logger.py            # Logger setup
│   └── token_counter.py     # Token counting for LLM
├── reports/                 # Generated reports
├── screenshots/             # Captured screenshots
└── ...
```

## Test Case Format
- Each test case in `test_case.json` should have:
```json
{
  "goal": "Description of the test",
  "action": "Step1. Step2. ..."
}
```
- Example:
```json
[
  {
    "goal": "Validate MC Login Page",
    "action": "Open the http://example.com/. Enter user in Login Id. Enter pass in Password. Click on the Login Button. Close the browser"
  }
]
```

## Notes
- **Gemini API Key:** The project expects a Gemini API key in the environment variable `GEMINI_API_KEY`. You can set it in your environment or directly in `main.py`.
- **Playwright Browsers:** After installing Playwright, run `playwright install` to download browser binaries.
- **Reports:** After running, check the `reports/automation_report.html` for results and screenshots.

## License
MIT 