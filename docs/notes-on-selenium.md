---
title: Notas sobre Selenium
---

## Introducción a Selenium

Selenium has three major tools.

1. Selenium IDE, a tool that reproduces scripts by recording and playing them back. Selenium IDE is
   more or less deprecated.

2. Selenium Server (Grid) for running tests in parallel on different machines.

3. **Selenium WebDriver**, a robust, browser-based regression automation suite, which enables
   distributing tests across many environments. 

## Selenium Webdriver

Selenium WebDriver supports many languages, including Python, C Sharp and Java and works with many browser types, operating systems and platforms, including mobile browsers, android, Windows, etc. However, the tester needs to be in sync with all the updates to ensure smooth testing.

Sample in Python::

```python
driver = webdriver.Firefox()
driver.get("http://www.parcan.es")
assert "Parlamento de Canarias" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("debate")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
assert "9L/DGEN-0002" in driver.page_source
driver.close()
```
