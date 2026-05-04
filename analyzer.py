import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Φόρτωση δεδομένων
print("📂 Φόρτωση δεδομένων...")
df = pd.read_csv('warehouse_data.csv')

# 2. Καθαρισμός (Data Cleaning) - Εδώ δείχνεις τις ικανότητές σου
print("🧹 Καθαρισμός δεδομένων...")
# Αντικαθιστούμε τα κενά Units_Sold με τον μέσο όρο (έξυπνη κίνηση)
df['Units_Sold'] = df['Units_Sold'].fillna(df['Units_Sold'].mean())
# Διαγράφουμε τις γραμμές που δεν έχουν Status
df = df.dropna(subset=['Status'])

# 3. Υπολογισμοί (Feature Engineering)
df['Total_Revenue'] = df['Units_Sold'] * df['Unit_Price']

# 4. Συμπεράσματα (Analytics)
top_products = df.groupby('Product')['Total_Revenue'].sum().sort_values(ascending=False)
print("\n💰 Συνολικά Έσοδα ανά Προϊόν:")
print(top_products)

# 5. Οπτικοποίηση (Visualizations)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_products.index, y=top_products.values)
plt.title('Total Revenue by Product')
plt.ylabel('Revenue ($)')
plt.savefig('revenue_chart.png')
print("\n📊 Το γράφημα 'revenue_chart.png' δημιουργήθηκε!")