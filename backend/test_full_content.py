#!/usr/bin/env python3
"""
Test that full content is being displayed in messages.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_full_content():
    """Create a task and check if full content is saved."""
    
    # Create a simple test task
    task_data = {
        "title": "Test Full Content Display",
        "description": "Create a short article about Python programming to test if full content is displayed"
    }
    
    print("Creating test task...")
    response = requests.post(f"{BASE_URL}/api/tasks/", json=task_data)
    if response.status_code != 201:
        print(f"Failed to create task: {response.text}")
        return
    
    task = response.json()
    task_id = task["id"]
    print(f"Task created: {task_id}")
    
    # Wait for completion
    print("Waiting for task to complete...")
    for i in range(60):
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
        if response.status_code == 200:
            task = response.json()
            if task["status"] == "completed":
                print("Task completed!")
                break
            elif task["status"] == "failed":
                print("Task failed!")
                return
        time.sleep(2)
        if i % 3 == 0:
            print(f"  Status: {task['status']} ({i*2}s elapsed)")
    
    # Get messages
    print("\nFetching messages...")
    response = requests.get(f"{BASE_URL}/api/messages/task/{task_id}")
    if response.status_code != 200:
        print(f"Failed to get messages: {response.text}")
        return
        
    data = response.json()
    messages = data["messages"]
    
    print(f"\nTotal messages: {len(messages)}")
    print("-" * 50)
    
    # Check for content from each agent
    writer_content = None
    analyst_content = None
    
    for msg in messages:
        agent = msg.get("agent_role", "unknown")
        content = msg.get("content", "")
        
        if agent == "writer" and "**Full Content:**" in content:
            writer_content = content
            print(f"\n✅ Writer sent full content ({len(content)} chars)")
            # Show first 200 chars
            print(f"Preview: {content[:200]}...")
            
        elif agent == "analyst" and "**Refined Content:**" in content:
            analyst_content = content
            print(f"\n✅ Analyst sent refined content ({len(content)} chars)")
            # Show first 200 chars
            print(f"Preview: {content[:200]}...")
    
    # Verify
    if writer_content and len(writer_content) > 500:
        print("\n✅ Writer content is complete (not truncated)")
    else:
        print("\n❌ Writer content appears truncated or missing")
        
    if analyst_content and len(analyst_content) > 500:
        print("✅ Analyst content is complete (not truncated)")
    else:
        print("❌ Analyst content appears truncated or missing")
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    test_full_content()