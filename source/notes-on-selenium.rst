Selenium
========================================================================


Introducción a Selenium
------------------------------------------------------------------------

Selenium has three major tools.

1. Selenium IDE, a tool that reproduces scripts by recording and playing
them back. Selenium IDE is more or less deprecated.

2. Selenium Server (Grid) for running tests in parallel on different
machines.

3. **Selenium WebDriver**, a robust, browser-based regression automation
suite, which enables distributing tests across many environments.


Selenium Webdriver
------------------------------------------------------------------------

*Selenium WebDriver* soporta varios lenguajes, incluyendo Python, C#
y Java, y funciona con diferentes familias de navegadores, sistemas
operativos y plataformas, incluyendo navegadores para móviles.

Ejemplo en Python:

.. code:: python

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Firefox()
    driver.get("https://www.gobiernodecanarias.org/buscador/search")
    assert "Gobierno de Canarias - Buscador" in driver.title
    elem = driver.find_element(By.ID, "query")
    elem.clear()
    elem.send_keys("Internet")
    elem.send_keys(Keys.RETURN)
    driver.close()
