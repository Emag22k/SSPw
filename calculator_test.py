from playwright.sync_api import sync_playwright
from time import sleep

def test_server_calculator():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, args= ["--incognito"])
        page = browser.new_page()
        page.goto('https://gcore.com/hosting')

        # Шаг 2: Прокручиваем страницу до области с кнопками
        page.evaluate('window.scrollTo(0, 800)')
        page.wait_for_timeout(2000)  # Ожидаем 2 секунды

        # Шаг 3: Ищем кнопку для выбора "Dedicated servers"
        dedicated_radio_button = page.locator('input.gc-switch-button-input[value="dedicated"]')

        # Проверка наличия кнопки на странице
        radio_button_count = dedicated_radio_button.count()
        if radio_button_count == 0:
            print("Радиокнопка 'Dedicated' не найдена на странице.")
            return

        # Шаг 4: Ожидаем, что радиокнопка станет доступной
        try:
            dedicated_radio_button.wait_for(state="visible", timeout=10000)
            print("Радиокнопка 'Dedicated' стала видимой.")
        except:
            print("Радиокнопка 'Dedicated' не стала видимой в течение 10 секунд.")
            return

        # Проверяем, что радиокнопка доступна для выбора
        assert dedicated_radio_button.is_enabled()
        assert dedicated_radio_button.is_visible()

        # Шаг 5: Кликаем по кнопке "Dedicated servers"
        dedicated_radio_button.click()

        # Шаг 6: Ищем кнопку для выбора валюты (USD)
        usd_currency_radio_button = page.locator('input[type="radio"][value="USD"]')

        # Ожидаем, что радиокнопка для валюты станет видимой
        try:
            usd_currency_radio_button.wait_for(state="visible", timeout=10000)
            print("Радиокнопка 'USD' стала видимой.")
        except:
            print("Радиокнопка 'USD' не стала видимой в течение 10 секунд.")
            return

        # Кликаем по кнопке для валюты USD
        usd_currency_radio_button.click()

        # Шаг 7: Проверяем, что выбранная валюта установлена
        selected_currency = page.locator('input[type="radio"][value="USD"]:checked')

        # Получаем атрибут 'value' у выбранной кнопки
        selected_value = selected_currency.get_attribute('value')
        print(f"Выбранная валюта: {selected_value}")
        assert selected_value == 'USD', f"Ожидалась валюта 'USD', но выбрана {selected_value}"

        # Шаг 8: Находим кнопку по тексту "Price" и нажимаем на нее
        button = page.locator('button >> text=Price')
        button.click()

      # Шаг 9: Выставляем минимальную и максимальную цену

        # Ждём, пока input'ы появятся
        page.wait_for_selector('input.gc-input[type="number"]')

        sleep(1)  #Даем странице обновить инпуты

        # Выбираем нужные поля
        min_input = page.locator('input.gc-input[type="number"]').nth(0)
        max_input = page.locator('input.gc-input[type="number"]').nth(1)


        # Чистим и вводим значение по одному символу
        min_input.click()
        min_input.press("Control+A")  # выделить всё
        min_input.press("Delete")  # удалить
        min_input.type("83", delay=100)  # ввод с задержкой
        min_input.press("Enter")  # подтверждение


        sleep(1) #Даем странице обновить инпуты

        max_input.click()
        max_input.press("Control+A")
        max_input.press("Delete")
        max_input.type("100", delay=100)
        max_input.press("Enter")

        sleep(2)  # Даем странице обновить серверы


        page.wait_for_timeout(5000)  # Задержка 5 секунд
        page.screenshot(path="screenshot.png")


        browser.close()

if __name__ == "__main__":
    test_server_calculator()

