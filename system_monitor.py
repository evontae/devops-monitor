''' Create a Python monitoring script incorporating the psutil module used to get system metrics, use tabulate to print data out in table format. We have datetime to get current time when script is ran. The json module outputs the metrics in json format which will later be used for enhancement. Lastly, pyinputplus handles user interaction on how the want the receieve the metrics'''
try:
    import psutil
    import shutil
    import datetime
    import json
    import tabulate
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')
    
def get_cpu_info():
    """
    This function gets information on the CPU, such as cores and usage.
    
    Error handling: access denial and general exceptions
    
    Arguments: None
    
    Returns: Dictionary with cpu information.
    
    Return Type: Dict
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

def get_memory_info():
    """
    This function gets information on memory, such as swap memory and the virtual usage.

    Error handling: access denial and general exceptions
    
    Arguments: None

    Returns: Dictionary with memory information.
    
    Return Type: Dict
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

def get_disk_info():
    """
    This function gets information on the disks, such as each partition and their usage.
    
    Error handling: access denial and general exceptions
    
    Arguments: None

    Returns: Dictionary with disk type and usage information.
    
    Return Type: Dict
    """
    try:
        disk_partitions = psutil.disk_partitions()
        disk_info = {"Disk Usage": {}}
        for partition in disk_partitions:
            try:  
                usage = shutil.disk_usage(partition.mountpoint)
            except Exception as e:
                print(f"Error getting disk usage for {partition.mountpoint}: {e}")
                continue  # Skip this partition and move on to the next
            # Check if percent attribute exists, if it doesn't then calculate it
            percent_used = usage.percent if hasattr(usage, "percent") else (usage.used / usage.total) * 100    
            disk_info["Disk Usage"][partition.mountpoint] = {
                "device": partition.device,
                "fstype": partition.fstype,
                "opts": partition.opts,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": round(percent_used, 1)
            }
        
        # Check if disk_info is empty after the loop
        if not disk_info["Disk Usage"]:
            print("Error: No accessible disk information found.")
            return {}

        return disk_info
    except psutil.AccessDenied:
        print(f"Error: Access denied to disk information.")
        return {}
    except Exception as error:
        print(f"Error: Unexpected error occurred in get_disk_info - {error}")
        return {}
    
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

def print_json(system_info: dict) -> str:
    """
    Prints system information in JSON format.

    Args:
        system_info (dict): A dictionary containing system information.

    Returns:
        str: The JSON string representation of the system information.
    """
    try:
        json_string = json.dumps(system_info, indent=4)
        print(json_string)
        return json_string
    except Exception as error:
        print(f"Error: An unexpected error occurred while printing JSON: {error}")
        return None
    
def print_table(system_info):
    """Prints system information in a tabular format."""

    current_time = datetime.datetime.now()
    print(f"\nSystem Monitor - {current_time}")

    # --- CPU Information Table ---
    try:
        cpu_headers = ["CPU", "User (%)", "System (%)", "Idle (%)"]
        cpu_table_data = [[cpu, info['user'], info['system'], info['idle']]
                          for cpu, info in system_info['cpu'].items()]
        print("\nCPU Information:")
        print(tabulate.tabulate(cpu_table_data, headers=cpu_headers, tablefmt="fancy_grid"))
    except Exception as e:
        print(f"Error printing CPU table: {e}")

    # --- Memory Information Table ---
    try:
        memory_headers = ["Metric", "Value (MB)"]
        memory_data = system_info['memory']['Memory']  
        memory_table_data = [
            ["Total", round(memory_data['total'] / 1024 / 1024, 2)],
            ["Available", round(memory_data['available'] / 1024 / 1024, 2)],
            ["Used", round(memory_data['used'] / 1024 / 1024, 2)],  # Corrected calculation
            ["Percent", round(memory_data['percent'], 1)]  
        ]
        print("\nMemory Information:")
        print(tabulate.tabulate(memory_table_data, headers=memory_headers, tablefmt="fancy_grid"))
    except KeyError as ke:  
        print(f"Error: Missing key in memory data: {ke}")
    except Exception as e:
        print(f"Error printing memory table: {e}")

    # --- Swap Memory Information Table ---
    try:
        swap_headers = ["Metric", "Value (MB)"]
        swap_data = system_info['memory']['Swap']  
        swap_table_data = [
            ["Total", swap_data['total'] / 1024 / 1024],
            ["Used", swap_data['used'] / 1024 / 1024],
            ["Free", swap_data['free'] / 1024 / 1024],
            ["Percent", swap_data['percent']]
        ]
        print("\nSwap Information:")
        print(tabulate.tabulate(swap_table_data, headers=swap_headers, tablefmt="fancy_grid"))
    except KeyError as ke:
        print(f"Error: Missing key in swap data: {ke}")
    except Exception as e:
        print(f"Error printing swap table: {e}")

    # --- Disk Information Table ---
    try:
        disk_headers = ["Mount Point", "Filesystem", "Size (GB)", "Used (GB)", "Free (GB)", "Percent (%)"]
        disk_table_data = []
        for mountpoint, info in system_info["disk"]["Disk Usage"].items():
            disk_table_data.append([mountpoint, info["fstype"], 
                                round(info["total"] / 1024 / 1024 / 1024, 2), 
                                round(info["used"] / 1024 / 1024 / 1024, 2),
                                round(info["free"] / 1024 / 1024 / 1024, 2),
                                round(info["percent"], 1) ])
        print("\nDisk Information:")
        print(tabulate.tabulate(disk_table_data, headers=disk_headers, tablefmt="fancy_grid"))
    except KeyError:
        print("Error: Disk information not available or in unexpected format.")
    except Exception as e:
        print(f"Error printing disk table: {e}")

    # --- Network Information Table ---
    try:
        network_headers = ["Metric", "Value"]
        network_table_data = [[k, v] for k, v in system_info['network'].items()]
        print("\nNetwork Information:")
        print(tabulate.tabulate(network_table_data, headers=network_headers, tablefmt="fancy_grid"))
    except KeyError:
        print("Error: Network information not available or in unexpected format.")
    except Exception as e:
        print(f"Error printing network table: {e}")

def print_monitor():
    """
    Retrieves and prints the system information.
    """
    current_time = datetime.datetime.now()

    system_info = {
        "timestamp" : current_time.isoformat(),
        "cpu" : get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network":get_network_info()
    }

    try:
        output_format = pyip.inputMenu(
            ['JSON', 'Table'], 
            prompt="Choose output format (json/table):\n", 
            numbered=True,
            allowRegexes=[r'^(json|table)$', 'i']  # Case-insensitive regex for validation
        ).lower()
    except pyip.ValidationError: 
        print("Invalid input. Please enter 'json' or 'table'.")
        return  # Exit function if input is invalid
    except Exception as error:
        print(f"Error getting user input: {error}. Defaulting to JSON output.")
        output_format = "json"

    if output_format == 'table':
        print_table(system_info) 
    else:
        result = print_json(system_info)
        if result is None:
            print("Error: Unable to generate JSON output.")


if __name__ == "__main__":
    print_monitor()