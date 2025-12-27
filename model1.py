# %%
import pandas as pd 

df = pd.read_csv("deployment_gate_training_v4.csv")
df = df.fillna(0)

print(df.shape)
df.head()

# %%
df["high_risk"] = (df["pipeline_success"]==0).astype(int)

df["high_risk"].value_counts(normalize=True)

# %%
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X = df.drop(columns=["pipeline_id","pipeline_success","high_risk"])
Y= df["high_risk"]

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=6,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1

)
scores = cross_val_score(rf,X,Y,cv=5,scoring="roc_auc")
print("AUC scores",scores.mean())



# %%
rf.fit(X,Y)
df["risk_score"] = rf.predict_proba(X)[:,1]
df[["risk_score"]].describe()

# %%
import pandas as pd 
import numpy as np

p80 = np.percentile(df["risk_score"],80)
p60 = np.percentile(df["risk_score"],60)

def deployment_gate(row):
    if row["is_production"]==1 and row["risk_score"]>=p80:
        return "BLOCK"
    elif row["risk_score"]>=p60:
        return "WARN"
    return "ALLOW"

df["gate_decision"] = df.apply(deployment_gate,axis=1)
df["gate_decision"].value_counts()



# %%
from sklearn.metrics import recall_score

failed = df["pipeline_success"] == 0
flagged = df["gate_decision"].isin(["BLOCK", "WARN"])

print(
    "Failure recall (BLOCK + WARN):",
    recall_score(failed, flagged)
)



