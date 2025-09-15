import time
import queue
import threading

# Event loop implementation
class EventLoop:
    def __init__(self):
        self.tasks = queue.Queue()
        self.running = False

    def call_later(self, delay, callback, *args):
        """Schedule a callback to run after a delay (in seconds)."""
        def delayed_task():
            time.sleep(delay)
            self.tasks.put((callback, args))
        threading.Thread(target=delayed_task).start()

    def call_soon(self, callback, *args):
        """Schedule a callback to run as soon as possible."""
        self.tasks.put((callback, args))

    def run_forever(self):
        """Run the event loop forever until stopped."""
        self.running = True
        while self.running:
            try:
                callback, args = self.tasks.get(timeout=0.1)
                callback(*args)
            except queue.Empty:
                continue

    def stop(self):
        self.running = False


# Example callbacks
def hello(name):
    print(f"Hello, {name}!")

def bye(name):
    print(f"Goodbye, {name}!")


# Example usage
if __name__ == "__main__":
    loop = EventLoop()

    # Schedule tasks
    loop.call_soon(hello, "Aakash")
    loop.call_later(2, bye, "Aakash")  # runs after 2 seconds

    # Start event loop
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
