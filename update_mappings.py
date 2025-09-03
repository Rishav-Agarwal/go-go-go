#!/usr/bin/env python3
"""
Helper script to update mappings.json in real-time.
Run this in a separate terminal while the main server is running.
"""

import json
import time

def add_mapping(name, url):
    """Add a new mapping to the file"""
    try:
        # Read existing mappings
        with open('mappings.json', 'r') as f:
            mappings = json.load(f)
        
        # Add new mapping
        mappings[name] = url
        
        # Write back to file
        with open('mappings.json', 'w') as f:
            json.dump(mappings, f, indent=4)
        
        print(f"Added mapping: go/{name} → {url}")
        return True
    except Exception as e:
        print(f"Error adding mapping: {e}")
        return False

def remove_mapping(name):
    """Remove a mapping from the file"""
    try:
        # Read existing mappings
        with open('mappings.json', 'r') as f:
            mappings = json.load(f)
        
        # Remove mapping
        if name in mappings:
            del mappings[name]
            
            # Write back to file
            with open('mappings.json', 'w') as f:
                json.dump(mappings, f, indent=4)
            
            print(f"Removed mapping: go/{name}")
            return True
        else:
            print(f"Mapping go/{name} not found")
            return False
    except Exception as e:
        print(f"Error removing mapping: {e}")
        return False

def show_mappings():
    """Show current mappings"""
    try:
        with open('mappings.json', 'r') as f:
            mappings = json.load(f)
        
        print("\nCurrent mappings:")
        for name, url in mappings.items():
            print(f"  go/{name} → {url}")
        print()
    except Exception as e:
        print(f"Error reading mappings: {e}")

if __name__ == "__main__":
    print("Go Links Mappings Manager")
    print("=========================")
    
    while True:
        print("\nOptions:")
        print("1. Add mapping")
        print("2. Remove mapping")
        print("3. Show mappings")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            name = input("Enter go/ link name: ").strip()
            url = input("Enter destination URL: ").strip()
            if name and url:
                add_mapping(name, url)
            else:
                print("Name and URL cannot be empty")
        
        elif choice == "2":
            name = input("Enter go/ link name to remove: ").strip()
            if name:
                remove_mapping(name)
            else:
                print("Name cannot be empty")
        
        elif choice == "3":
            show_mappings()
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")
