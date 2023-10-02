# Import necessary modules and libraries
import time
import multiprocessing

# Import your custom script modules
from data_collector import collect_all_metrics

# Define a function for your main script
def main():
    # Create separate processes for data collection, processing, and transmission
    data_collection_process = multiprocessing.Process(target=collect_all_metrics)

    # Start the processes
    data_collection_process.start()

    try:
        # Add any additional logic or control flow here as needed

        # In this example, the main script will run indefinitely,
        # but you can customize this based on your project's requirements.
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # Handle a keyboard interrupt (e.g., Ctrl+C) to gracefully exit the processes
        data_collection_process.terminate()
        data_collection_process.join()

if __name__ == "__main__":
    main()
