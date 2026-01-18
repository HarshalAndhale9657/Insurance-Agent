import sys
import os
import uuid

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.report_service import generate_pdf_report

def test_pdf_generation():
    print("📄 Testing PDF Generation Service...")
    
    dummy_data = {
        "name": "Rajesh Kumar",
        "age": "35",
        "occupation": "Farmer",
        "family": "4 Members",
        "worry": "Crop Failure"
    }
    
    recommendation = (
        "Based on your profile, I recommend the **PMFBY Crop Insurance Scheme**.\n"
        "It covers yield losses due to non-preventable risks like drought and floods.\n"
        "Premium is only 2% for Kharif crops."
    )
    
    filename = f"Test_Report_{uuid.uuid4().hex[:6]}.pdf"
    
    try:
        path = generate_pdf_report(dummy_data, recommendation, filename)
        if os.path.exists(path):
            print(f"✅ PDF Generated Successfully: {path}")
            print(f"📂 Size: {os.path.getsize(path)} bytes")
        else:
            print("❌ File created but not found on disk.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pdf_generation()
