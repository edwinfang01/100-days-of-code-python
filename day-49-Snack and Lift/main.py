import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

ACCOUNT_EMAIL = "loool@gmail.com"
ACCOUNT_PASSWORD = "idkajao"
GYM_URL = "https://appbrewery.github.io/gym/"

driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)

wait = WebDriverWait(driver, timeout=2)

def login():
    global wait
    login_button = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

    email_input = wait.until(ec.presence_of_element_located((By.NAME, "email")))
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button#submit-button")))
    submit_button.click()

    wait.until(ec.presence_of_element_located(locator=(By.CSS_SELECTOR, "#schedule-page")))

def retry(func, retries=7, description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt {i+1}")
        try:
            return func()
        except TimeoutException:
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

def book_class(booking_button):
    booking_button.click()
    wait.until(
        lambda _: booking_button.text == "Booked" or booking_button.text == "Waitlisted"
    )

retry(login,description="login")

class_details = []
classes_booked, waitlists_joined, already_booked, total_classes_processed = (0,0,0,0)
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

for class_card in class_cards:

    day_group = class_card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    date = day_group.find_element(By.TAG_NAME, "h2").text
    if "Wed" in date or "Thu" in date:

        time_text = class_card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "7:00 AM" in time_text:
            booked = class_card.get_attribute("data-user-booked") == "true"
            in_waitlist = class_card.get_attribute("data-user-waitlisted") == "true"
            is_full = class_card.get_attribute("data-is-fully-booked") == "true"
            class_type: str = class_card.get_attribute("data-class-type").capitalize()

            if booked:
                print(f"✓ Already booked: {class_type} on {date}")
            elif in_waitlist:
                print(f"✓ Already on waitlist: {class_type} on {date}")
            elif is_full:
                button = class_card.find_element(By.TAG_NAME, "button")
                retry(lambda: book_class(button), description="Waitlisting")
                print(f"✓ Joined waitlist for: {class_type} on {date}")
                class_details.append(f"  • [New Waitlist] {class_type} on {date}")
                waitlists_joined += 1

            else:
                button = class_card.find_element(By.TAG_NAME, "button")
                retry(lambda: book_class(button), description="Booking")
                print(f"✓ Successfully booked: {class_type} on {date}")
                class_details.append(f"  • [New Booking] {class_type} on {date}")
                classes_booked += 1

            already_booked += int(booked) + int(in_waitlist)
            waitlists_joined += int(in_waitlist)
            total_classes_processed += 1

success_string = ""
my_bookings = []
def get_my_bookings():
    global success_string, my_bookings
    my_bookings_button = driver.find_element(By.ID, "my-bookings-link")
    my_bookings_button.click()
    wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

    my_bookings = driver.find_elements(By.CSS_SELECTOR, "div[id^='booking-card-booking']") + driver.find_elements(By.CSS_SELECTOR, "div[id^='waitlist-card-waitlist']")
    def verify_text(booking):
        return "Wed" in booking.find_element(By.XPATH, ".//p[strong[text()='When:']]").text or "Thu" in booking.find_element(By.XPATH, ".//p[strong[text()='When:']]").text

    my_bookings = [booking for booking in my_bookings if verify_text(booking)]
    missing_bookings = len(class_details) + already_booked -len(my_bookings)
    success_string = "✅ Success: All bookings verified!" if missing_bookings == 0 else f"❌ MISMATCH: Missing {missing_bookings} bookings"

retry(get_my_bookings, description="get my bookings")

print(f"""
--- BOOKING SUMMARY ---
Classes booked: {classes_booked}
Waitlists joined: {waitlists_joined}
Already booked/waitlisted: {already_booked}
Total classes processed: {total_classes_processed}

--- DETAILED CLASS LIST ---
{"\n".join(class_details)}

--- VERIFICATION RESULT ---
Expected: {len(class_details)}
Found: {len(my_bookings)}
{success_string}
"""
)
