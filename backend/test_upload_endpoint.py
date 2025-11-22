"""
Example script to test the file upload endpoint for plagiarism detection.

Usage:
    python test_upload_endpoint.py <file_path>

Example:
    python test_upload_endpoint.py example.py
"""

import requests
import sys
import os


def test_upload_endpoint(
    file_path: str,
    api_url: str = "http://localhost:8000"
):
    """
    Test the /api/v1/upload endpoint by uploading a file for check.

    Args:
        file_path: Path to the Python file to check
        api_url: Base URL of the API (default: http://localhost:8000)
    """
    endpoint = f"{api_url}/api/v1/upload"

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found")
        return

    print(f"📤 Uploading file: {file_path}")
    print("🔗 Endpoint: " + endpoint)
    print("-" * 60)

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/plain')}
            response = requests.post(endpoint, files=files)

        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print("\n📊 Results:")
            print(f"   Success: {result.get('success')}")

            comparisons = result.get('comparisons', [])
            if comparisons:
                comp_count = len(comparisons)
                print(f"\n🔍 Found {comp_count} comparison(s):")
                for i, comp in enumerate(comparisons, 1):
                    print(f"\n   [{i}] Block: {comp.get('block_name')}")
                    similarity = comp.get('similarity_percent')
                    print(f"       Similarity: {similarity}%")
                    if comp.get('source_repo'):
                        print(f"       Source: {comp.get('source_repo')}")
                    if comp.get('source_url'):
                        print(f"       URL: {comp.get('source_url')}")
                    if comp.get('reason'):
                        print(f"       Reason: {comp.get('reason')}")
            else:
                print("\n✨ No plagiarism detected!")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Cannot connect to {api_url}")
        print("   Make sure the server is running with:")
        print("   uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_upload_endpoint.py <file_path>")
        print("\nExample:")
        print("  python test_upload_endpoint.py example.py")
        sys.exit(1)

    file_path = sys.argv[1]
    test_upload_endpoint(file_path)
