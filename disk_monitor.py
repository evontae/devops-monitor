try:
    import psutil
    import shutil
    import json
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')

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