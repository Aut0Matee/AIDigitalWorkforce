#!/usr/bin/env python3
"""
Test that markdown content is properly formatted in messages.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_markdown_test_task():
    """Create a task that will generate markdown content."""
    
    task_data = {
        "title": "Markdown Rendering Test",
        "description": "Create a document with various markdown elements: headings, lists, bold text, code blocks, and links to test rendering"
    }
    
    print("Creating test task with markdown requirements...")
    response = requests.post(f"{BASE_URL}/api/tasks/", json=task_data)
    if response.status_code != 201:
        print(f"Failed to create task: {response.text}")
        return None
    
    task = response.json()
    task_id = task["id"]
    print(f"✅ Task created: {task_id}")
    
    # Give it time to generate some messages
    print("Waiting for agents to generate markdown content...")
    time.sleep(10)
    
    # Get messages
    response = requests.get(f"{BASE_URL}/api/messages/task/{task_id}")
    if response.status_code != 200:
        print(f"Failed to get messages: {response.text}")
        return None
        
    data = response.json()
    messages = data["messages"]
    
    print(f"\n📝 Found {len(messages)} messages")
    print("-" * 50)
    
    # Check for markdown elements
    markdown_elements = {
        "headings": ["#", "##", "###"],
        "bold": ["**", "__"],
        "lists": ["- ", "* ", "1. "],
        "code": ["```", "`"],
        "links": ["[", "]("],
    }
    
    for msg in messages:
        agent = msg.get("agent_role", "unknown")
        content = msg.get("content", "")
        
        if len(content) > 100:  # Only check substantial messages
            print(f"\n[{agent}] Message contains:")
            found_elements = []
            
            for element_type, markers in markdown_elements.items():
                for marker in markers:
                    if marker in content:
                        found_elements.append(element_type)
                        break
            
            if found_elements:
                print(f"  ✅ Markdown elements: {', '.join(set(found_elements))}")
                # Show a snippet
                snippet = content[:200].replace('\n', ' ')
                print(f"  Preview: {snippet}...")
            else:
                print(f"  ⚠️  No markdown elements detected")
    
    print("\n" + "=" * 50)
    print("Markdown Test Complete!")
    print("Check the frontend at http://localhost:3000 to verify proper rendering")
    print("=" * 50)
    
    return task_id

if __name__ == "__main__":
    task_id = create_markdown_test_task()
    if task_id:
        print(f"\n🔗 View task at: http://localhost:3000/task/{task_id}")