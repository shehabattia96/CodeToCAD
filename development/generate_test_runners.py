import os
import sys
# Add the parent directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from development.utilities import to_snake_case


# Define the path to the __init__.py file and the output directory
init_file_path = 'tests/test_providers/sample_implemented/__init__.py'
output_dir = 'tests/test_runners'

# Read the __init__.py file
with open(init_file_path, 'r') as file:
    lines = file.readlines()

# Extract class names from the __init__.py file
class_names = []
for line in lines:
    if line.startswith('from .') and 'import' in line:
        # Extract the class name from the import statement
        class_name = line.split('import')[-1].strip().split()[0]
        class_names.append(class_name)

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Generate test runner files for each class
for class_name in class_names:
    # Convert class name to snake case for the file name
    snake_case_name = to_snake_case(class_name)
    test_runner_file_path = os.path.join(output_dir, f'test_run_{snake_case_name}.py')
    
    with open(test_runner_file_path, 'w') as test_file:
        test_file.write(f"""import unittest
import tests.test_providers.sample_implemented as sample_implemented

try:
    unittest.main(argv=["-v", "sample_implemented.{class_name}"], exit=False)
except Exception as e:
    print(e)
""")

print(f"Test runner files created in '{output_dir}' for classes: {', '.join(class_names)}")