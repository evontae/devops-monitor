
try:
    import psutil
    import shutil
    import json
    import pyinputplus as pyip
except ImportError as import_error:
    print(f'Error importing module: {import_error}')

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