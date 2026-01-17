import subprocess
import sys
import os

def main():
    """
    Entry point to run the Streamlit application.
    """
    app_path = os.path.join(os.path.dirname(__file__), "app", "main.py")
    print(f"Starting Insurance Agent App from: {app_path}")
    
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except KeyboardInterrupt:
        print("\nStopping application...")
    except FileNotFoundError:
        print("Error: 'streamlit' command not found. Please ensure it is installed via 'pip install -r requirements.txt'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
