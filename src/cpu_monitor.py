"""
This module provides functions for monitoring CPU metrics.

Functions:
    get_cpu_info(): Returns a dictionary containing information about CPU utilization.
"""

try:
    import psutil
    import shutil
    import json
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')
    
def get_cpu_info():
    """
    Returns a dictionary containing information about CPU utilization.

    Returns:
        dict: A dictionary with keys representing CPU core numbers (e.g., 'cpu1', 'cpu2')
              and values containing dictionaries with the following metrics:
              - user: Percentage of time spent in user mode
              - system: Percentage of time spent in system mode
              - idle: Percentage of time spent idle
    """
    try:
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_times_percent(percpu=True)
        cpu_information =  {}
        for cpu_index, cpu in enumerate(cpu_percent):
            cpu_information[f'cpu{cpu_index+1}'] = cpu._asdict()
        return cpu_information
    except psutil.AccessDenied:
        print("Error: Access denied to CPU information.")
        return {}  
    except Exception as error:  
        print(f"Error: Unexpected error occurred - {error}")
        return {}   