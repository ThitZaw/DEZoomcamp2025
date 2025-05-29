import time

def print_hello_every_minute():
    for _ in range(60):  # Loop 60 times for 60 minutes
        print("Hello")
        time.sleep(60)  # Wait for 60 seconds

print_hello_every_minute()
