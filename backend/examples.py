import requests
from app.agents.orchestrator import Orchestrator


def example_basic_usage():
    """Basic example of using the plagiarism detector"""

    code_sample = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
"""

    orchestrator = Orchestrator()
    result = orchestrator.execute_pipeline(code_sample)

    print("=== Plagiarism Detection Results ===\n")

    if result["success"]:
        print(f"Total blocks analyzed: {result['total_blocks']}\n")

        print("Similarity Analysis:")
        for comparison in result["comparisons"]:
            print(f"\n  Block: {comparison['block_name']}")
            print(f"  Type: {comparison['block_type']}")
            print(f"  Similarity: {comparison['similarity_percent']}%")
            print(f"  Suspicious: {comparison['is_suspicious']}")

            if comparison["source_repo"]:
                print(f"  Source: {comparison['source_repo']}")
                print(f"  URL: {comparison['source_url']}")
                print(f"  Reason: {comparison['reason']}")
    else:
        print(f"Error: {result['error']}")


def example_stage_by_stage():
    """Example showing intermediate results from each stage"""

    code_sample = """
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)
"""

    orchestrator = Orchestrator()
    result = orchestrator.execute_pipeline(code_sample)

    print("=== Stage-by-Stage Results ===\n")

    if result.get("stage_1_result"):
        stage_1 = result["stage_1_result"]
        print("Stage 1 - Code Splitter:")
        print(f"  Total blocks: {stage_1['total_blocks']}")
        for block in stage_1['blocks']:
            print(f"  - {block['type']}: {block['name']}")

    if result.get("stage_2_result"):
        stage_2 = result["stage_2_result"]
        print("\nStage 2 - Git Searcher:")
        for search in stage_2['search_results']:
            matches = search['found_matches']
            block_name = search['block_name']
            print(f"  - {block_name}: {len(matches)} matches found")
            for match in matches[:1]:
                print(f"    └─ {match['repo']}")

    if result.get("stage_3_result"):
        stage_3 = result["stage_3_result"]
        print("\nStage 3 - Similarity Finder:")
        for comp in stage_3['comparisons']:
            similarity = comp['similarity_percent']
            print(f"  - {comp['block_name']}: {similarity}% similar")


def example_empty_code():
    """Example handling empty code"""

    orchestrator = Orchestrator()

    try:
        result = orchestrator.execute_pipeline("")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error handled: {e}")


def example_code_without_functions():
    """Example with simple code without functions"""

    code_sample = """
x = 10
y = 20
z = x + y
print(z)
"""

    orchestrator = Orchestrator()
    result = orchestrator.execute_pipeline(code_sample)

    print("=== Simple Code Analysis ===\n")

    if result["success"]:
        print(f"Blocks found: {result['total_blocks']}")
        for comp in result["comparisons"]:
            similarity = comp['similarity_percent']
            print(
                f"Block '{comp['block_name']}': {similarity}% similar"
            )


def example_api_file_upload():
    """Example of using the file upload API endpoint"""

    api_url = "http://localhost:8000/api/v1/upload"
    file_path = "example_code.py"

    print("=== File Upload API Example ===\n")
    print(f"Uploading: {file_path}")
    print(f"Endpoint: {api_url}\n")

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'text/plain')}
            response = requests.post(api_url, files=files)

        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!\n")

            if result['success']:
                comparisons = result.get('comparisons', [])
                print(f"Found {len(comparisons)} comparison(s):\n")

                for i, comp in enumerate(comparisons, 1):
                    print(f"[{i}] {comp['block_name']}")
                    print(f"    Similarity: {comp['similarity_percent']}%")
                    if comp.get('source_repo'):
                        print(f"    Source: {comp['source_repo']}")
                    if comp.get('reason'):
                        print(f"    Reason: {comp['reason']}")
                    print()
            else:
                print(f"Error: {result.get('error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")

    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        msg = "Create example_code.py first or use "
        msg += "test_upload_endpoint.py script"
        print(msg)
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {api_url}")
        print("Make sure the server is running:")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Example 1: Basic Usage")
    print("-" * 50)
    try:
        example_basic_usage()
    except Exception as e:
        print(f"Note: Requires valid API keys. Error: {e}")

    print("\n\nExample 2: Stage-by-Stage")
    print("-" * 50)
    try:
        example_stage_by_stage()
    except Exception as e:
        print(f"Note: Requires valid API keys. Error: {e}")

    print("\n\nExample 3: Empty Code Handling")
    print("-" * 50)
    example_empty_code()

    print("\n\nExample 4: Code without Functions")
    print("-" * 50)
    try:
        example_code_without_functions()
    except Exception as e:
        print(f"Note: Requires valid API keys. Error: {e}")

    print("\n\nExample 5: File Upload API")
    print("-" * 50)
    try:
        example_api_file_upload()
    except Exception as e:
        msg = "Note: Requires server running and example_code.py."
        print(f"{msg} Error: {e}")
