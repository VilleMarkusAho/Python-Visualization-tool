import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib==3.4.2'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyQt5'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'git+https://github.com/anntzer/mplcursors'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print('installed packages:')
print(installed_packages)
