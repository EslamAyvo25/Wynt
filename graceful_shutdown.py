import signal
import asyncio

# Flag to control the running state of the service
is_running = True


def graceful_shutdown(signum, frame):
    global is_running
    print(f"\nReceived signal {signum}, shutting down gracefully...")
    tasks = asyncio.all_tasks()
    if len(tasks) == 0:
        print("\nShutdown now \n")
        is_running = False

# Service logic (replace this with your service code)
async def run_service():
    global is_running
    print("Service is running...")
    count = 5
    while count:
        print("Service is still running...")
        count -=1
        await asyncio.sleep(1)  # Simulate work

    print("Service has stopped.")

async def main():
    # Register signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, graceful_shutdown, signal.SIGINT, None)  # Handle Ctrl+C (SIGINT)
    loop.add_signal_handler(signal.SIGTERM, graceful_shutdown, signal.SIGTERM, None)  # Handle termination (SIGTERM)

    await run_service()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nService interrupted manually.")
    finally:
        print("Graceful shutdown complete.")
