"""
Example Python script with intentional bugs for testing Code Review Crew.

This file contains various bugs, security issues, and performance problems
to demonstrate the capabilities of the AI code review system.
"""

import os
import json
import hashlib
import random


# SECURITY ISSUE: Hardcoded credentials
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
DATABASE_PASSWORD = "admin123"


class UserManager:
    def __init__(self):
        self.users = []

    # BUG: Missing docstring and type hints
    def calculate_average_age(self, ages):
        total = sum(ages)
        # BUG: Division by zero if ages is empty
        average = total / len(ages)
        return average

    # SECURITY: SQL Injection vulnerability
    def get_user_by_id(self, user_id):
        # CRITICAL: SQL injection - user_id not sanitized
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return self.execute_query(query)

    # SECURITY: Weak cryptography
    def hash_password(self, password):
        # SECURITY: MD5 is not suitable for passwords
        return hashlib.md5(password.encode()).hexdigest()

    # SECURITY: Insecure random for tokens
    def generate_token(self):
        # SECURITY: random module not cryptographically secure
        return str(random.randint(100000, 999999))

    # BUG: None handling issue
    def get_user_name(self, user):
        name = user.get('name')
        # BUG: What if name is None?
        return name.upper()

    def execute_query(self, query):
        # Placeholder
        pass


# PERFORMANCE: Inefficient nested loops (O(n²))
def find_duplicates(data):
    duplicates = []
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j and data[i] == data[j]:
                if data[i] not in duplicates:
                    duplicates.append(data[i])
    return duplicates


# PERFORMANCE: String concatenation in loop
def build_report(items):
    report = ""
    # PERFORMANCE: O(n²) - creates new string each time
    for item in items:
        report += f"Item: {item}\n"
    return report


# BUG: List modification during iteration
def remove_negative_numbers(numbers):
    for num in numbers:
        if num < 0:
            # BUG: Modifying list while iterating causes skipping
            numbers.remove(num)
    return numbers


# BUG: Missing error handling
def load_config(filename):
    # BUG: File operations without try-except
    with open(filename) as f:
        config = json.loads(f.read())
    return config


# BUG: Resource leak
def read_large_file(filepath):
    # BUG: File not using context manager
    f = open(filepath, 'r')
    data = f.readlines()
    # BUG: File never closed
    return data


# SECURITY: Command injection
def ping_host(hostname):
    # SECURITY: Command injection vulnerability
    os.system(f"ping -c 1 {hostname}")


# PERFORMANCE: Not using set for membership testing
def check_membership(item, items_list):
    # PERFORMANCE: O(n) lookup instead of O(1) with set
    if item in items_list:
        return True
    return False


# BUG: Off-by-one error
def get_first_n_items(items, n):
    result = []
    # BUG: range should be range(n) not range(n+1)
    for i in range(n + 1):
        if i < len(items):
            result.append(items[i])
    return result


# DOCUMENTATION: Missing docstring, unclear variable names
def process(d, x, y):
    r = d * x + y
    return r


# BUG: Mutable default argument
def append_to_list(item, my_list=[]):
    # BUG: Default mutable argument persists across calls
    my_list.append(item)
    return my_list


# PERFORMANCE: Redundant computation
def calculate_stats(data):
    results = []
    # PERFORMANCE: len(data) called multiple times
    for i in range(len(data)):
        if data[i] > 0:
            results.append(data[i] / len(data))
    return results


# BUG: Broad exception handling
def risky_operation():
    try:
        # Some risky operation
        result = 10 / 0
        return result
    except:
        # BUG: Bare except catches everything, including KeyboardInterrupt
        pass


# SECURITY: Path traversal vulnerability
def read_user_file(filename):
    # SECURITY: No validation of filename - path traversal possible
    with open(f"/data/{filename}", 'r') as f:
        return f.read()


# Main execution
if __name__ == "__main__":
    manager = UserManager()

    # Example usage with bugs
    ages = []  # Empty list will cause division by zero
    avg = manager.calculate_average_age(ages)

    data = [1, 2, 3, 2, 4, 3, 5]
    dupes = find_duplicates(data)

    print("Script completed")
