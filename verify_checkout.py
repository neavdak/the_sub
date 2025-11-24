import requests
from bs4 import BeautifulSoup

def verify_checkout():
    session = requests.Session()
    # Login
    login_url = 'http://127.0.0.1:5000/login'
    session.post(login_url, data={'username': 'admin', 'password': 'password'})

    # Get initial balance
    profile_url = 'http://127.0.0.1:5000/profile'
    response = session.get(profile_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    balance_text = soup.find('div', class_='balance-amount').text.strip().replace('$', '')
    initial_balance = float(balance_text)
    print(f"Initial Balance: ${initial_balance}")

    # Buy 1 fraction of Property 1
    # We need to know the price. Let's assume Property 1 exists and has fractions.
    # Property 1 (Downtown Apartment): Value 100000, Fractions 100 => Price 1000
    buy_url = 'http://127.0.0.1:5000/buy/1'
    response = session.post(buy_url, data={'fractions': '1'})
    
    if "Purchase Successful!" in response.text:
        print("Purchase successful page loaded.")
    else:
        print("Failed to load success page.")
        # print(response.text) # Debug if needed

    # Verify balance deduction
    response = session.get(profile_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    balance_text = soup.find('div', class_='balance-amount').text.strip().replace('$', '')
    new_balance = float(balance_text)
    print(f"New Balance: ${new_balance}")

    expected_balance = initial_balance - 1000
    if abs(new_balance - expected_balance) < 0.01:
        print("Balance deduction verified.")
    else:
        print(f"Balance mismatch. Expected: {expected_balance}, Got: {new_balance}")

if __name__ == "__main__":
    try:
        verify_checkout()
    except Exception as e:
        print(f"Verification failed: {e}")
