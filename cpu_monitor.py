try:
    import psutil
    import shutil
    import json
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