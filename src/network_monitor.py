"""
This module provides functions for monitoring network metrics.

Functions:
    get_memory_info(): Returns a dictionary containing information about network utilization.
"""

try:
    import psutil
    import shutil
    import json
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')

def get_network_info():
    """
    Retrieves information about network traffic statistics.

    Error handling: Includes checks for access denial and general exceptions.

    Arguments: None

    Returns:
        dict: A dictionary containing network traffic metrics:
            
            - Bytes Sent: (int) Total number of bytes sent over the network.
            - Bytes Received: (int) Total number of bytes received from the network.
            - Packets Sent: (int) Total number of packets sent.
            - Packets Received: (int) Total number of packets received.

    Raises:
        psutil.AccessDenied: If permission is denied to access network information.
        Exception: For any other unexpected errors encountered during metric collection.
    """
    try:
        network_usage = psutil.net_io_counters()
        return {
            "Bytes Sent":network_usage.bytes_sent,
            "Bytes Received":network_usage.bytes_recv,
            "Packets Sent": network_usage.packets_sent,
            "Packets Received": network_usage.packets_recv
        }
    except psutil.AccessDenied:
        print(f"Error: Access denied to network information.")  
        return {}  
    except Exception as error:
        print(f"Error: Unexpected error occurred in get_network_info - {error}") 
        return {}