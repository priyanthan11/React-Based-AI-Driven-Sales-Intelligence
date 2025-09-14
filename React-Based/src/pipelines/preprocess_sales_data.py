import pandas as pd
import sys

# ---- Config: expected (logical) column names ----
REQUIRED_COLS = {
    "opportunity_id",
    "sales_agent",
    "product",
    "account",
    "deal_stage",
    "engage_date",
    "close_date",
    "close_value",
}

# ---- Load data ----
csv_path = "./data/raw/sales_pipeline.csv"
df = pd.read_csv(csv_path)

# ---- 1) Normalize column names to a safe canonical form ----
# Example: " Sales Agent " -> "sales_agent", "CloseDate" -> "closedate" -> "close_date"


def canonicalize(col_name: str) -> str:
    s = col_name.strip()                       # remove leading/trailing spaces
    s = s.replace("\ufeff", "")                # remove BOM if present
    s = s.replace("-", " ").replace(".", " ")  # normalize separators
    # collapse whitespace -> single underscore
    s = "_".join(s.split())
    return s.lower()


orig_cols = list(df.columns)
col_map = {c: canonicalize(c) for c in orig_cols}
df = df.rename(columns=col_map)

# ---- 2) Check for required columns ----
missing = REQUIRED_COLS - set(df.columns)
if missing:
    print("ERROR: The following required columns are missing (after normalisation):")
    for c in missing:
        print(f"  - {c}")
    print("\nAvailable columns found in CSV (after normalisation):")
    for c in df.columns:
        print(f"  - {c}")
    print("\nSuggestions:")
    print("  * Confirm CSV header matches expected column names (case/spacing).")
    print("  * If your CSV uses different names, map them manually. Example mapping:")
    print(
        "      df = df.rename(columns={'sales rep': 'sales_agent', 'closeDate': 'close_date'})")
    # Stop execution to avoid creating misleading features
    sys.exit(1)

# ---- 3) Cleaning (safe assignments) ----
df = df.drop_duplicates(subset="opportunity_id")
df["close_value"] = df["close_value"].fillna(df["close_value"].median())

# ---- 4) Convert dates (coerce errors so we can see problematic rows) ----
df["engage_date"] = pd.to_datetime(df["engage_date"], errors="coerce")
df["close_date"] = pd.to_datetime(df["close_date"], errors="coerce")

# Optional: print any rows with bad dates for inspection
bad_dates = df[df["engage_date"].isna() | df["close_date"].isna()]
if not bad_dates.empty:
    print("WARNING: Some rows have invalid or unparsable dates (engage_date / close_date).")
    print(bad_dates[["opportunity_id", "engage_date", "close_date"]].head(10))
    # decide whether to drop or handle them; here we drop to keep pipeline moving
    df = df.dropna(subset=["engage_date", "close_date"]).reset_index(drop=True)

# ---- 5) Feature engineering (do group-by and lag BEFORE encoding) ----
df["deal_duration_days"] = (df["close_date"] - df["engage_date"]).dt.days
df["engage_month"] = df["engage_date"].dt.month
df["engage_quarter"] = df["engage_date"].dt.quarter
df["engage_year"] = df["engage_date"].dt.year

# Agent stats
agent_stats = (
    df.groupby("sales_agent")
      .agg(
          agent_total_deals=("opportunity_id", "count"),
          agent_won_deals=("deal_stage", lambda x: (x == "Won").sum()),
          agent_avg_deal_value=("close_value", "mean")
    )
    .reset_index()
)
agent_stats["agent_win_rate"] = agent_stats["agent_won_deals"] / \
    agent_stats["agent_total_deals"]
df = df.merge(agent_stats, on="sales_agent", how="left")

# Account stats
account_stats = (
    df.groupby("account")
      .agg(
          account_total_deals=("opportunity_id", "count"),
          account_avg_deal_value=("close_value", "mean")
    )
    .reset_index()
)
df = df.merge(account_stats, on="account", how="left")

# Sort and compute lag features
df = df.sort_values(["sales_agent", "engage_date"]).reset_index(drop=True)
df["prev_deal_value_agent"] = df.groupby(
    "sales_agent")["close_value"].shift(1).fillna(0)

# High value flag
df["is_high_value"] = (
    df["close_value"] > df["close_value"].mean()).astype(int)

# ---- 6) Encoding (do this last) ----
# For small cardinality: one-hot. For production with high-cardinality, prefer target encoding.
df = pd.get_dummies(
    df, columns=["sales_agent", "product", "account"], drop_first=True)

# ---- 7) Final housekeeping ----
df = df.reset_index(drop=True)
print("Preprocessing completed. Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Optionally save processed dataset
df.to_parquet("./data/processed/sales_pipeline_processed.parquet", index=False)
print("Saved processed dataset to ./data/processed/sales_pipeline_processed.parquet")
