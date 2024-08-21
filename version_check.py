import os
import re

# Directory containing your Python files
directory = "/Users/johnfirnschild/Documents/HomeLab/Python/projects/games/tower_defense"

# Regex pattern to match the version variable (version = "X.X.X")
version_pattern = re.compile(r'version\s*=\s*[\'"]([^\'"]+)[\'"]', re.IGNORECASE)

def find_versions_in_files(directory):
    versions = {}
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Check if the file has a .py extension
        if filename.endswith('.py'):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r') as file:
                content = file.read()
                match = version_pattern.search(content)
                if match:
                    versions[filename] = match.group(1)
                else:
                    versions[filename] = "Version not found"
    
    return versions

# Run the version lookup
versions = find_versions_in_files(directory)
for file, version in versions.items():
    print(f"{file}: {version}")