from app import create_app
import traceback

try:
    app = create_app()
    print("App created successfully")
except Exception:
    traceback.print_exc()
