#!/usr/bin/env python3
"""
Test that all agent messages are being saved to the database.
"""

import asyncio
import requests
import time
import json

BASE_URL = "http://localhost:8000"

def create_test_task():
    """Create a test task."""
    task_data = {
        "title": "Test Message Persistence",
        "description": "Quick test to verify all agent messages are saved to database"
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks/", json=task_data)
    if response.status_code == 201:
        task = response.json()
        print(f"✅ Task created: {task['id']}")
        return task['id']
    else:
        print(f"❌ Failed to create task: {response.text}")
        return None

def wait_for_completion(task_id, max_wait=60):
    """Wait for task to complete."""
    print("Waiting for task to complete...")
    for i in range(max_wait):
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
        if response.status_code == 200:
            task = response.json()
            status = task['status']
            if status == 'completed':
                print(f"✅ Task completed")
                return True
            elif status == 'failed':
                print(f"❌ Task failed")
                return False
            else:
                if i % 5 == 0:
                    print(f"  Status: {status} ({i}s elapsed)")
        time.sleep(1)
    
    print(f"⏱️ Task did not complete within {max_wait} seconds")
    return False

def check_messages(task_id):
    """Check messages for the task."""
    response = requests.get(f"{BASE_URL}/api/messages/task/{task_id}")
    if response.status_code == 200:
        data = response.json()
        messages = data['messages']
        
        print(f"\n📬 Total messages saved: {len(messages)}")
        print("\nMessage breakdown by agent:")
        
        agent_counts = {}
        for msg in messages:
            agent = msg.get('agent_role', 'unknown')
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
            
        for agent, count in agent_counts.items():
            print(f"  {agent}: {count} messages")
        
        print("\nMessage timeline:")
        for i, msg in enumerate(messages, 1):
            agent = msg.get('agent_role', 'unknown')
            content_preview = msg.get('content', '')[:100]
            if len(msg.get('content', '')) > 100:
                content_preview += "..."
            print(f"  {i}. [{agent}] {content_preview}")
        
        # Check for expected messages
        expected_min_messages = 5  # At least initial messages from each agent
        if len(messages) >= expected_min_messages:
            print(f"\n✅ All messages appear to be saved (found {len(messages)} messages)")
            return True
        else:
            print(f"\n❌ Missing messages (expected at least {expected_min_messages}, found {len(messages)})")
            return False
    else:
        print(f"❌ Failed to get messages: {response.text}")
        return False

def main():
    print("=" * 50)
    print("Testing Message Persistence")
    print("=" * 50)
    
    # Create task
    task_id = create_test_task()
    if not task_id:
        return
    
    # Wait for completion
    if not wait_for_completion(task_id):
        return
    
    # Check messages
    time.sleep(2)  # Give a moment for final saves
    check_messages(task_id)
    
    print("\n" + "=" * 50)
    print("Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    main()