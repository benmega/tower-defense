import os
import inspect
import importlib.util

def get_class_names(directory):
    class_names = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    continue
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        class_names.append(obj.__name__)
    return class_names


# Example usage
directory = 'C:\\Users\\Ben\\PycharmProjects\\towerDefense\\src'  # Replace with the path to your project
print(get_class_names(directory))
