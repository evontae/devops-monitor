"""
This module provides functions for monitoring disk metrics.

Functions:
    get_dick_info(): Returns a dictionary containing information about disk utilization.
"""

try:
    import psutil
    import shutil
    import json
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')

def get_disk_info():
    """
    Returns a dictionary containing information about disk utilization.

    Returns:
        dict: A "Disk Usage" dictionary containing keys representing mount points (e.g., 'C:\\', '/dev/sda1')
              and values containing dictionaries with the following metrics:
              - device: The device name associated with the mount point.
              - fstype: The file system type (e.g., NTFS, ext4).
              - opts: Mount options (e.g., rw,fixed).
              - total: Total disk size in bytes.
              - used: Used disk space in bytes.
              - free: Free disk space in bytes.
              - percent: Percentage of disk space used (0.0 to 100.0).
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