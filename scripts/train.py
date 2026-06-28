import argparse 
from core.data.features import get_features
from core.models.laptime_model import train_final_model, train_with_cv,save_model,predict_lap_time


def main(refresh):
    print("="*50)
    print("RaceEngineerAI-Training Pipeline")
    print("="*50)
    features = get_features(force_refresh=refresh)
    print(features["Track"].unique())
    print(features["RaceId"].nunique())
    print(f"\nDataset:{len(features)} laps,{features['RaceId'].nunique()} races")
   
    print("\n---Cross Validation---")
    metrics = train_with_cv(features)
    print(f"Mean MAE:{metrics['mean_mae']:.3f}s (+/-{metrics['std_mae']:.3f}s)")

    print("\n--- Training Final Model ---")
    pipeline = train_final_model(features)
    save_model(pipeline,metrics)

    print("\n--- Sanity Check ---")
    pred = predict_lap_time(
        pipeline,track="Monaco",driver="VER",
        compound="SOFT", lap_number=10, tyre_life=5,stint=1
    )
    print(f"Monaco | VER | SOFT | Lap 10 | TyreLife ->{pred:.3f}s predicted")

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--refresh",action="store_true",help="Force re-fetch from FastF1")
    args = parser.parse_args()
    main(refresh=args.refresh)
