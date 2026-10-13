n_exact = df.duplicated().sum()
print(f"Exact duplicate rows: {n_exact}")
df = df.drop_duplicates()

# Duplicates defined by identifying fields (adjust to your data)
key = ["src_ip", "dst_ip", "src_port", "dst_port", "timestamp"]
n_key = df.duplicated(subset=key).sum()
print(f"Duplicates on key fields: {n_key}")
df = df.drop_duplicates(subset=key, keep="first")
