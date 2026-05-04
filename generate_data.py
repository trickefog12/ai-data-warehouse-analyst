import pandas as pd
import numpy as np

# Δημιουργία τυχαίων δεδομένων για μια αποθήκη
data = {
    'Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
    'Product': np.random.choice(['Sensor A', 'Controller B', 'Valve C', 'Cable D'], 100),
    'Units_Sold': np.random.randint(1, 50, 100),
    'Unit_Price': [15.5, 120.0, 45.0, 12.0] * 25,
    'Status': np.random.choice(['Shipped', 'Pending', 'Cancelled'], 100, p=[0.7, 0.2, 0.1])
}

df = pd.DataFrame(data)

# Εισαγωγή "λαθών" (Missing values) για να δείξουμε ότι ξέρουμε να καθαρίζουμε δεδομένα
df.loc[5:10, 'Units_Sold'] = np.nan
df.loc[20:22, 'Status'] = None

df.to_csv('warehouse_data.csv', index=False)
print("✅ Το αρχείο 'warehouse_data.csv' δημιουργήθηκε με επιτυχία!")