try:
    import datetime
    import json
    import tabulate
    import pyinputplus as pyip
    
    from cpu_monitor import get_cpu_info
    from memory_monitor import get_memory_info
    from disk_monitor import get_disk_info
    from network_monitor import get_network_info
except ImportError as import_error:
    print(f'Error importing module: {import_error}')

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