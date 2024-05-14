"""
This module provides functions for monitoring memory metrics.

Functions:
    get_memory_info(): Returns a dictionary containing information about memory utilization.
"""

try:
    import psutil
    import shutil
    import json
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')

def get_memory_info():
    """
    Retrieves information about system memory and swap memory usage.

    Error handling: Includes checks for access denial and general exceptions.

    Arguments: None

    Returns:
        dict: A dictionary containing memory and swap information, structured as follows:
              
              - "Memory": (dict)
                  - total: (int) Total physical memory in bytes.
                  - available: (int) Available memory in bytes.
                  - used: (int) Memory currently in use in bytes.
                  - percent: (float) Percentage of memory used (0.0 to 100.0).

              - "Swap": (dict)
                  - total: (int) Total swap space in bytes.
                  - used: (int) Swap space currently in use in bytes.
                  - free: (int) Available swap space in bytes.
                  - percent: (float) Percentage of swap space used (0.0 to 100.0).

    Raises:
        psutil.AccessDenied: If permission is denied to access memory information.
        Exception: For any other unexpected errors encountered during metric collection.
    """
    try:
        memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        return {
            "Memory": {
                "total":memory.total,
                "available": memory.available,
                "used":memory.used,
                "percent":memory.percent
            },
            "Swap": {
                "total":swap_memory.total,
                "used": swap_memory.used,
                "free":swap_memory.free,
                "percent":swap_memory.percent
            }          
        }   
    except psutil.AccessDenied:
        print(f"Error: Access denied to memory information.")  
        return {}  
    except Exception as error:
        print(f"Error: Unexpected error occurred in get_memory_info - {error}") 
        return {}