import json
import os
from bs4 import BeautifulSoup
import google.generativeai as genai
import logging

class LocatorManager:
    def __init__(self, cache_file, model, token_counter):
        self.cache_file = cache_file
        self.model = model
        self.token_counter = token_counter
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get_locator(self, element_description, page_content, save_cache=False):
        # Try cache first
        if element_description in self.cache:
            return self.cache[element_description]
        # Try LLM
        locator = self._get_locator_from_llm(element_description, page_content)
        if locator and locator != 'null':
            self.cache[element_description] = locator
            if save_cache:
                self.save_cache()
            return locator
        # Try alternative strategies (self-healing)
        locator = self._try_alternatives(element_description, page_content)
        if locator:
            self.cache[element_description] = locator
            if save_cache:
                self.save_cache()
            return locator
        return None

    def _get_locator_from_llm(self, element_description, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')
        simplified_dom = []
        for element in soup.find_all(['input', 'button', 'div', 'span','a','label']):
            attrs = {
                'tag': element.name,
                'id': element.get('id', ''),
                'class': ' '.join(element.get('class', [])),
                'text': element.get_text(strip=True)[:50],
                'name': element.get('name', ''),
                'type': element.get('type', '')
            }
            simplified_dom.append(attrs)
        # print("simplified_dom: "+ simplified_dom)
        prompt = (
            f"You are an expert in web automation. Given the following simplified webpage DOM elements:\n"
            f"{json.dumps(simplified_dom, indent=2)}\n"
            f"Generate a Playwright-compatible locator (Xpath selector,CSS selector or text-based selector) for an element described as: '{element_description}'.\n"
            f"Return only the locator string (e.g., 'input[name=vik]' or 'input[name=sss]') or 'input[id=sss]' or 'button[id=fdd]' or '//a[@id=221]' or 'input[value='dfd']' or 'null' if no suitable locator is found.\n"
            f"Do not include any additional text or explanation."
        )
        self.token_counter.add(prompt)
        try:
            print("prompt: "+ prompt)
            logging.info(f"Prompt: '{prompt}'")
            response = self.model.generate_content(prompt)
            locator = response.text.strip()
            logging.info(f"Gemini LLM returned locator '{locator}' for '{element_description}'")
            return locator
        except Exception as e:
            logging.error(f"Error in Gemini LLM locator extraction: {str(e)}")
            return None

    def _try_alternatives(self, element_description, page_content):
        # Self-healing: try text, CSS, XPath
        soup = BeautifulSoup(page_content, 'html.parser')
        # Try by text
        for tag in ['button', 'a', 'span', 'div', 'label']:
            for el in soup.find_all(tag):
                if element_description.lower() in el.get_text(strip=True).lower():
                    if el.get('id'):
                        return f"{tag}#" + el.get('id')
                    if el.get('class'):
                        return f"{tag}." + '.'.join(el.get('class'))
                    return f"text={el.get_text(strip=True)}"
        # Try by name or id for inputs
        for el in soup.find_all('input'):
            if el.get('name') and element_description.lower() in el.get('name').lower():
                return f"input[name={el.get('name')}]"
            if el.get('id') and element_description.lower() in el.get('id').lower():
                return f"input[id={el.get('id')}]"
        return None 