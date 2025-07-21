import sys
import sklearn
import pandas
import numpy

print("--- ENVIRONMENT CHECK ---")
try:
    print(f"Python Executable:    {sys.executable}")
    print(f"Scikit-learn version: {sklearn.__version__}")
    print(f"Pandas version:       {pandas.__version__}")
    print(f"NumPy version:        {numpy.__version__}")
except Exception as e:
    print(f"An error occurred: {e}")
print("-------------------------")