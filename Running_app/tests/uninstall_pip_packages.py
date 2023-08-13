import subprocess

with open('installed_packages.txt', 'r') as file:
    for line in file:
        package = line.strip()
        subprocess.run(['pip', 'uninstall', '-y', package])
