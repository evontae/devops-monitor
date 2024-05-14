try:
    import psutil
    import shutil
    import json
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')

def get_network_info():
    """
    This function gets information on network metrics, the bytes and packets.
    
    Error handling: access denial and general exceptions
    
    Arguments: None

    Returns: Dictionary with network information on data sent and received.
    
    Return Type: Dict
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