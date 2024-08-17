import importlib
import inspect
import os
import sys
from typing import Dict, Any, List


def meta(**metadata):
    def decorator(func):
        if not hasattr(func, "meta"):
            func.meta = []
        func.meta.append(metadata)
        return func

    return decorator


def compile_function_metadata(current_handler_dir: str) -> List[Dict[str, Any]]:
    tools = []
    functions_dir = os.path.join(current_handler_dir, "functions")

    if not os.path.isdir(functions_dir):
        return tools

    if functions_dir not in sys.path:
        sys.path.insert(0, functions_dir)

    function_files = [f[:-3] for f in os.listdir(functions_dir) if f.endswith(".py") and not f.startswith("__")]

    for module_name in function_files:
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if hasattr(obj, "meta"):
                for meta_info in obj.meta:
                    tools.append({"type": "function", "function": meta_info})

    sys.path.remove(functions_dir)

    return tools


def compile_function_map(current_handler_dir: str) -> Dict[str, Any]:
    function_map = {}
    functions_dir = os.path.join(current_handler_dir, "functions")

    if not os.path.isdir(functions_dir):
        return function_map

    if functions_dir not in sys.path:
        sys.path.insert(0, functions_dir)

    function_files = [f[:-3] for f in os.listdir(functions_dir) if f.endswith(".py") and not f.startswith("__")]

    for module_name in function_files:
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if hasattr(obj, "meta"):
                function_map[name] = obj

    sys.path.remove(functions_dir)

    return function_map
