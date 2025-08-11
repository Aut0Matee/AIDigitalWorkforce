#!/usr/bin/env python3
"""
Test script to verify the content truncation and empty message fixes.
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

async def test_content_truncation():
    """Test that content writer agent doesn't truncate content."""
    print("\n=== Testing Content Truncation Fix ===")
    
    async with aiohttp.ClientSession() as session:
        # Create a task that should generate long content
        task_data = {
            "title": "Write a comprehensive guide on Pakistan's EV market",
            "description": "Create a detailed 2000+ word article about Pakistan's electric vehicle market, covering government policies, local startups, challenges, opportunities, and future prospects. Include statistics and data."
        }
        
        print(f"Creating task: {task_data['title']}")
        async with session.post(f"{API_URL}/tasks/", json=task_data) as resp:
            if resp.status != 201:
                print(f"Failed to create task: {await resp.text()}")
                return False
            
            task = await resp.json()
            task_id = task["id"]
            print(f"Task created with ID: {task_id}")
            
        # Wait for task to complete (max 60 seconds)
        print("Waiting for task to complete...")
        for i in range(60):
            await asyncio.sleep(1)
            async with session.get(f"{API_URL}/tasks/{task_id}") as resp:
                task = await resp.json()
                if task["status"] == "completed":
                    break
                if i % 5 == 0:
                    print(f"  Status: {task['status']} ({i}s elapsed)")
        
        if task["status"] != "completed":
            print(f"Task did not complete in time. Status: {task['status']}")
            return False
            
        # Check deliverable length
        deliverable = task.get("deliverable", "")
        word_count = len(deliverable.split())
        char_count = len(deliverable)
        
        print(f"\nDeliverable stats:")
        print(f"  Character count: {char_count}")
        print(f"  Word count: {word_count}")
        print(f"  First 200 chars: {deliverable[:200]}...")
        print(f"  Last 200 chars: ...{deliverable[-200:]}")
        
        # Check if content seems truncated
        if char_count < 3000:
            print("❌ Content appears truncated (less than 3000 characters)")
            return False
        
        if deliverable.endswith("...") or deliverable.endswith(".."):
            print("❌ Content appears truncated (ends with ellipsis)")
            return False
            
        print("✅ Content appears complete!")
        return True

async def test_empty_messages():
    """Test that empty messages don't appear when viewing tasks."""
    print("\n=== Testing Empty Messages Fix ===")
    
    async with aiohttp.ClientSession() as session:
        # Get existing tasks
        async with session.get(f"{API_URL}/tasks/") as resp:
            data = await resp.json()
            tasks = data.get("tasks", [])
            
        if not tasks:
            print("No existing tasks to test with")
            return False
            
        # Check messages for each task
        for task in tasks[:3]:  # Check first 3 tasks
            task_id = task["id"]
            print(f"\nChecking messages for task: {task['title']}")
            
            async with session.get(f"{API_URL}/messages/task/{task_id}") as resp:
                if resp.status != 200:
                    print(f"  Failed to get messages: {await resp.text()}")
                    continue
                    
                data = await resp.json()
                messages = data.get("messages", [])
                
                empty_count = 0
                for msg in messages:
                    content = msg.get("content", "")
                    if not content or not content.strip():
                        empty_count += 1
                        print(f"  ❌ Found empty message from {msg.get('agent_role', 'unknown')}")
                
                if empty_count == 0:
                    print(f"  ✅ No empty messages found ({len(messages)} total messages)")
                else:
                    print(f"  ❌ Found {empty_count} empty messages out of {len(messages)} total")
                    return False
                    
        print("\n✅ No empty messages found in any tasks!")
        return True

async def main():
    """Run all tests."""
    print("Starting content fix tests...")
    print(f"Testing against: {BASE_URL}")
    
    results = []
    
    # Test content truncation fix
    result1 = await test_content_truncation()
    results.append(("Content Truncation Fix", result1))
    
    # Test empty messages fix
    result2 = await test_empty_messages()
    results.append(("Empty Messages Fix", result2))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + ("All tests passed! 🎉" if all_passed else "Some tests failed. Please review the fixes."))
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)