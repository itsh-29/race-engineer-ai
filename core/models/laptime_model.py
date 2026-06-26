import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
from core.config import CATEGORICAL_FEATURES,METRICS_PATH,MODEL_PATH,NUMERIC_FEATURES,TARGET


def build_pipeline():
    preprocessor = ColumnTransformer(transformers=[
        ("cat",OneHotEncoder(handle_unknown="ignore"),CATEGORICAL_FEATURES),
        ("num","passthrough",NUMERIC_FEATURES)
    ])

    model = XGBRegressor(
        n_estimators=400,
        max_depth= 6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state =42,
        n_jobs=-1
    )
    return Pipeline([("preprocess",preprocessor),("model",model)])

def train_with_cv(df,n_splits=5):
    x = df[CATEGORICAL_FEATURES+NUMERIC_FEATURES]
    y = df[TARGET]
    groups = df["RaceId"]
    n_splits = min(n_splits,df["RaceId"].nunique())
    gkf = GroupKFold(n_splits=n_splits)
    fold_score= []
    for fold,(train_idx,test_idx) in enumerate(gkf.split(x,y,groups)):
        pipeline = build_pipeline()
        pipeline.fit(x.iloc[train_idx],y.iloc[train_idx])
        preds = pipeline.predict(x.iloc[test_idx])
        mae = mean_absolute_error(y.iloc[test_idx],preds)
        fold_score.append(mae)
        print(f"Fold {fold+1}: MAE={mae:.3f}s")
    metrics ={
        "fold_mae":fold_score,
        "mean_mae":float(np.mean(fold_score)),
        "std_mae" :float(np.std(fold_score)),
        "n_sample":len(df),
        "n_races" :int(df["RaceId"].nunique()), 
    }     
    return metrics

def train_final_model(df):
    X = df[CATEGORICAL_FEATURES+NUMERIC_FEATURES]
    y = df[TARGET]
    pipeline = build_pipeline()
    pipeline.fit(X,y)
    return pipeline

def save_model(pipeline,metrics):
    joblib.dump(pipeline,MODEL_PATH)
    with open(METRICS_PATH,"w") as f:
        json.dump(metrics,f,indent=2)
    print(f"Model saved to{MODEL_PATH}")

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("No Trained model found.Run scripts/train.py first.")
    return joblib.load(MODEL_PATH)

def predict_lap_time(pipeline,track,driver,compound,lap_number,tyre_life,stint=1):
    row = pd.DataFrame([{
        "Track": track,
        "Driver": driver,
        "Compound":compound,
        "LapNumber":lap_number,
        "TyreLife": tyre_life,
        "Stint":stint,
    }]) 
    return float(pipeline.predict(row)[0])