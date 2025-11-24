# The Sub

A Flask-based web application.

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/neavdak/the_sub.git
    cd the_sub
    ```

2.  **Create a virtual environment (optional but recommended):**

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the server:**

    ```bash
    python run.py
    ```

2.  **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:5000`.

### Additional Scripts

-   `seed_history.py`: Seeds the database with history data.
-   `add_admin_funds.py`: Adds funds to the admin account.
-   `verify_checkout.py`: Verifies checkout functionality.