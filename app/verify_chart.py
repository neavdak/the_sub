import requests
import json

def verify_chart_api():
    session = requests.Session()
    # Login not strictly needed for this API if I didn't protect it, but good practice
    # API is public in my implementation
    
    # Check Property 1 history
    url = 'http://127.0.0.1:5000/api/history/1'
    try:
        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                print(f"API returned {len(data)} data points.")
                print(f"First point: {data[0]}")
                print(f"Last point: {data[-1]}")
            else:
                print("API returned empty list.")
        else:
            print(f"API failed with status {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    verify_chart_api()
