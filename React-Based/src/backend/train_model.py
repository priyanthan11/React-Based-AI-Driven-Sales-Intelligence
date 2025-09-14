import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import xgboost as xgb
import lightgbm as lgb
import joblib

# Leand processed data
# "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/data/processed/sales_pipeline_processed.parquet"
df = pd.read_parquet(
    "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/data/processed/sales_pipeline_processed.parquet")

print(df.head())

# Define target and features
target = "deal_stage"  # assuming 1= win, 0 = lost

X = df.drop(columns=["opportunity_id", "deal_stage", target, "engage_date",
                     "close_date"])


y = df[target] = df["deal_stage"].map({"Won": 1, "Lost": 0})

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train: XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric="logloss",
)

xgb_model.fit(X_train, y_train)

# ---- Option B: LightGBM ----
# lgb_model = lgb.LGBMClassifier(
#     n_estimators=500,
#     learning_rate=0.05,
#     num_leaves=31,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     random_state=42,
# )
# lgb_model.fit(X_train, y_train)

FEATURE_COLUMNS = X_train.columns.tolist()
joblib.dump(FEATURE_COLUMNS,
            "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/models/feature_columns.pkl")


# Evaluate
y_pred = xgb_model.predict(X_test)
y_prob = xgb_model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# Save model
joblib.dump(
    xgb_model, "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/models/xgb_sales_model.pkl")
print("Saved XGBoost model to ./models/xgb_sales_model.pkl")
