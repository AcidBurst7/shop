#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Добавляем путь к DLL прямо в системный PATH текущего процесса Python
msys_path = r'C:\\msys64\\mingw64\\bin'
if msys_path not in os.environ['PATH']:
    os.environ['PATH'] = msys_path + os.pathsep + os.environ['PATH']

# Явный флаг для WeasyPrint
os.environ['WEASYPRINT_DLL_DIRECTORIES'] = msys_path

# Для Python 3.8+ на Windows нужно явно разрешить загрузку DLL из этой папки
if sys.platform == 'win32' and hasattr(os, 'add_dll_directory'):
    try:
        os.add_dll_directory(msys_path)
    except FileNotFoundError:
        pass

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
