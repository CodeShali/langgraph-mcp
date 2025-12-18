"""
Test script for the MCP server
This script tests all the MCP server endpoints to ensure they're working correctly.
"""

import requests
import json
import sys

MCP_SERVER_URL = "http://localhost:5000"


def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print("✗ Health check failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_list_tools():
    """Test listing available tools"""
    print("\n" + "=" * 60)
    print("TEST 2: List Tools")
    print("=" * 60)
    
    try:
        response = requests.get(f"{MCP_SERVER_URL}/tools", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            tools = response.json().get("tools", [])
            print(f"\n✓ Found {len(tools)} tools")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
            return True
        else:
            print("✗ List tools failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_add_tool():
    """Test the add tool"""
    print("\n" + "=" * 60)
    print("TEST 3: Add Tool (15 + 27)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/add",
            json={"a": 15, "b": 27},
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json().get("result")
            expected = 42
            if result == expected:
                print(f"✓ Add tool passed: {result} == {expected}")
                return True
            else:
                print(f"✗ Add tool failed: {result} != {expected}")
                return False
        else:
            print("✗ Add tool failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_subtract_tool():
    """Test the subtract tool"""
    print("\n" + "=" * 60)
    print("TEST 4: Subtract Tool (100 - 37)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/subtract",
            json={"a": 100, "b": 37},
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json().get("result")
            expected = 63
            if result == expected:
                print(f"✓ Subtract tool passed: {result} == {expected}")
                return True
            else:
                print(f"✗ Subtract tool failed: {result} != {expected}")
                return False
        else:
            print("✗ Subtract tool failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_multiply_tool():
    """Test the multiply tool"""
    print("\n" + "=" * 60)
    print("TEST 5: Multiply Tool (8 * 9)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/multiply",
            json={"a": 8, "b": 9},
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json().get("result")
            expected = 72
            if result == expected:
                print(f"✓ Multiply tool passed: {result} == {expected}")
                return True
            else:
                print(f"✗ Multiply tool failed: {result} != {expected}")
                return False
        else:
            print("✗ Multiply tool failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_tool_call_endpoint():
    """Test the generic tool call endpoint"""
    print("\n" + "=" * 60)
    print("TEST 6: Generic Tool Call Endpoint (add 5 + 3)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/call",
            json={
                "tool_name": "add",
                "arguments": {"a": 5, "b": 3}
            },
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json().get("result")
            expected = 8
            if result == expected:
                print(f"✓ Tool call endpoint passed: {result} == {expected}")
                return True
            else:
                print(f"✗ Tool call endpoint failed: {result} != {expected}")
                return False
        else:
            print("✗ Tool call endpoint failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_error_handling():
    """Test error handling with invalid tool"""
    print("\n" + "=" * 60)
    print("TEST 7: Error Handling (invalid tool)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/invalid_tool",
            json={"a": 5, "b": 3},
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 404:
            print("✓ Error handling passed: correctly returned 404")
            return True
        else:
            print(f"✗ Error handling failed: expected 404, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 60)
    print("MCP SERVER TEST SUITE")
    print("=" * 60)
    print(f"Testing server at: {MCP_SERVER_URL}")
    
    tests = [
        test_health_check,
        test_list_tools,
        test_add_tool,
        test_subtract_tool,
        test_multiply_tool,
        test_tool_call_endpoint,
        test_error_handling
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    # Check if server is accessible
    try:
        requests.get(f"{MCP_SERVER_URL}/health", timeout=2)
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR: Cannot connect to MCP server")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nPlease make sure the MCP server is running:")
        print("  python mcp_server.py")
        print("=" * 60)
        sys.exit(1)
    
    # Run tests
    exit_code = run_all_tests()
    sys.exit(exit_code)
