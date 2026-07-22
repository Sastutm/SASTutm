import os, re
import glob

pattern = re.compile(r'threading\.Thread\(\s*target=(email_service\.\w+),\s*args=\(([^)]+)\),\s*daemon=True\s*\)\.start\(\)', re.MULTILINE)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = pattern.sub(lambda m: f'{m.group(1)}({m.group(2).rstrip(",")})', content)
    
    new_content = re.sub(r'threading\.Thread\(target=(email_service\.\w+), args=\(([^)]+)\), daemon=True\)\.start\(\)', lambda m: f'{m.group(1)}({m.group(2).rstrip(",")})', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')

for root, _, files in os.walk('app/blueprints'):
    for file in files:
        if file.endswith('.py'):
            process_file(os.path.join(root, file))
