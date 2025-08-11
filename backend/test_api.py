#!/usr/bin/env python3
"""
Test script to verify all API endpoints are working correctly.
"""

import asyncio
import json
import sys
from typing import Dict, Any
import httpx
from datetime import datetime

import os
BASE_URL = os.environ.get("API_URL", "http://localhost:8001")
TIMEOUT = httpx.Timeout(30.0)

async def test_health_check() -> bool:
    """Test the health check endpoint."""
    print("\n1. Testing Health Check...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Health check passed: {data}")
                return True
            else:
                print(f"   ❌ Health check failed: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
            return False

async def test_api_docs() -> bool:
    """Test that API documentation is accessible."""
    print("\n2. Testing API Documentation...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(f"{BASE_URL}/docs")
            if response.status_code == 200:
                print(f"   ✅ API docs available at {BASE_URL}/docs")
                return True
            else:
                print(f"   ❌ API docs not accessible: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ API docs error: {e}")
            return False

async def test_create_task() -> Dict[str, Any]:
    """Test creating a new task."""
    print("\n3. Testing Task Creation...")
    task_data = {
        "title": "Test Task - Summarize AI trends",
        "description": "Research and summarize the top 3 AI trends in 2025"
    }
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/api/tasks/",
                json=task_data
            )
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Task created successfully: ID={data.get('id')}")
                return data
            else:
                print(f"   ❌ Task creation failed: Status {response.status_code}")
                print(f"      Response: {response.text}")
                return {}
        except Exception as e:
            print(f"   ❌ Task creation error: {e}")
            return {}

async def test_get_tasks() -> bool:
    """Test retrieving task list."""
    print("\n4. Testing Get Tasks...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/tasks/")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Retrieved {data.get('total', 0)} tasks")
                if data.get('tasks'):
                    print(f"      Sample task: {data['tasks'][0]['title']}")
                return True
            else:
                print(f"   ❌ Get tasks failed: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Get tasks error: {e}")
            return False

async def test_get_task_detail(task_id: str) -> bool:
    """Test retrieving a specific task."""
    print(f"\n5. Testing Get Task Detail (ID: {task_id})...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/tasks/{task_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Task retrieved: {data.get('title')}")
                print(f"      Status: {data.get('status')}")
                return True
            else:
                print(f"   ❌ Get task detail failed: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Get task detail error: {e}")
            return False

async def test_get_messages(task_id: str) -> bool:
    """Test retrieving messages for a task."""
    print(f"\n6. Testing Get Messages (Task ID: {task_id})...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/messages/task/{task_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Retrieved {data.get('total', 0)} messages")
                return True
            else:
                print(f"   ❌ Get messages failed: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Get messages error: {e}")
            return False

async def test_websocket_connection() -> bool:
    """Test WebSocket connectivity."""
    print("\n7. Testing WebSocket Connection...")
    try:
        import socketio
        sio = socketio.AsyncClient()
        
        connected = False
        
        @sio.event
        async def connect():
            nonlocal connected
            connected = True
            print("   ✅ WebSocket connected successfully")
        
        @sio.event
        async def connect_error(data):
            print(f"   ❌ WebSocket connection error: {data}")
        
        try:
            await sio.connect(f"{BASE_URL}")
            await asyncio.sleep(2)  # Wait for connection
            
            if connected:
                await sio.disconnect()
                return True
            else:
                print("   ❌ WebSocket failed to connect")
                return False
        except Exception as e:
            print(f"   ❌ WebSocket error: {e}")
            return False
            
    except ImportError:
        print("   ⚠️  python-socketio not installed, skipping WebSocket test")
        return False

async def test_delete_task(task_id: str) -> bool:
    """Test deleting a task."""
    print(f"\n8. Testing Delete Task (ID: {task_id})...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.delete(f"{BASE_URL}/api/tasks/{task_id}")
            if response.status_code == 200:
                print(f"   ✅ Task deleted successfully")
                return True
            else:
                print(f"   ❌ Delete task failed: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Delete task error: {e}")
            return False

async def main():
    """Run all API tests."""
    print("=" * 60)
    print("AI Digital Workforce - API Testing Suite")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    
    results = {
        "health_check": False,
        "api_docs": False,
        "create_task": False,
        "get_tasks": False,
        "get_task_detail": False,
        "get_messages": False,
        "websocket": False,
        "delete_task": False
    }
    
    # Run tests
    results["health_check"] = await test_health_check()
    results["api_docs"] = await test_api_docs()
    
    # Create a test task
    task_data = await test_create_task()
    if task_data and task_data.get("id"):
        results["create_task"] = True
        task_id = task_data["id"]
        
        # Test other endpoints with the created task
        results["get_tasks"] = await test_get_tasks()
        results["get_task_detail"] = await test_get_task_detail(task_id)
        results["get_messages"] = await test_get_messages(task_id)
        results["websocket"] = await test_websocket_connection()
        
        # Clean up - delete the test task
        results["delete_task"] = await test_delete_task(task_id)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title():.<40} {status}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The API is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the backend logs.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)