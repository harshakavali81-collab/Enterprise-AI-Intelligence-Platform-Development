"""Create reproducible held-out synthetic model-vs-baseline evaluations and charts.

These tests do NOT estimate safety, impact or accuracy on real users.
"""
import json
from pathlib import Path
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score,precision_score,recall_score,accuracy_score
from app.classification import SCAM_TRAIN, ISSUE_TRAIN
from app.forecasting import forecast
from app.engine import SYNTH_SERIES

OUT=Path("reports")
HELD_OUT={
"scam": [
("Please send me the updated agenda by tomorrow",0),
("Team meeting is now on Thursday afternoon",0),
("Your account is suspended, confirm OTP to proceed",1),
("Click this prize claim link and pay a fee",1),
("Thank you for sharing the project documentation",0),
("Transfer money now to avoid account suspension",1),
("Attached are the lecture notes for students",0),
("Verify your credentials with this password reset link",1),
],
"civic": [
("There is a huge crater on the carriageway","pothole"),
("Road hole makes cycling hard","pothole"),
("Lamp post is dark and fails at night","streetlight"),
("The roadway street light is broken","streetlight"),
("Access to the ramp is obstructed","blocked_access"),
("Disabled entrance has been blocked","blocked_access"),
("Sidewalk slabs have come apart","footpath"),
("Walking pavement surface is cracked","footpath")
]
}
def model_baselines(kind,train,holdout):
    X_train,y_train=zip(*train)
    X_test,y_test=zip(*holdout)
    model=make_pipeline(TfidfVectorizer(ngram_range=(1,2)),
                        LogisticRegression(max_iter=600,random_state=11))
    model.fit(X_train,y_train)
    baseline=DummyClassifier(strategy="most_frequent").fit([[0] for _ in X_train],y_train)
    result={"dataset":"fictional held-out authored examples",
            "train_size":len(train),"test_size":len(holdout),"results":{}}
    for name,pred in [("tfidf_logistic",model.predict(X_test)),
                      ("most_frequent_baseline",baseline.predict([[0] for _ in X_test]))]:
        result["results"][name]={
            "accuracy":round(float(accuracy_score(y_test,pred)),4),
            "macro_precision":round(float(precision_score(y_test,pred,average="macro",zero_division=0)),4),
            "macro_recall":round(float(recall_score(y_test,pred,average="macro",zero_division=0)),4),
            "macro_f1":round(float(f1_score(y_test,pred,average="macro",zero_division=0)),4),
            "prediction_errors":[{"input":x,"expected":str(y),"predicted":str(p)}
                                 for x,y,p in zip(X_test,y_test,pred) if y!=p]
        }
    return result

def svg_report(rows):
    # Deterministic chart generated from computed test scores, not fictional plotted values.
    width=960
    height=140+len(rows)*95
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
         '<rect width="100%" height="100%" fill="#090909"/>',
         '<text x="34" y="45" fill="#D4AF65" font-size="26" font-family="Arial">SYNTHETIC HOLDOUT · MODEL VS BASELINE</text>',
         '<text x="34" y="70" fill="#F5F0E6" font-size="15" font-family="Arial">Macro F1 on small fictional test sets; no real-world performance claim.</text>']
    for i,(name,model,baseline) in enumerate(rows):
        y=110+i*95
        label=name.replace("_"," ").upper()
        out.extend([
            f'<text x="35" y="{y}" fill="#F5F0E6" font-size="17" font-family="Arial">{label}</text>',
            f'<rect x="260" y="{y-18}" width="{round(model*520)}" height="20" fill="#D4AF65"/>',
            f'<rect x="260" y="{y+13}" width="{round(baseline*520)}" height="18" fill="#6E6556"/>',
            f'<text x="{268+round(model*520)}" y="{y-3}" fill="#F5F0E6" font-size="14" font-family="Arial">{model:.3f} MODEL</text>',
            f'<text x="{268+round(baseline*520)}" y="{y+27}" fill="#B8B4AC" font-size="14" font-family="Arial">{baseline:.3f} NAIVE</text>'])
    out.append('</svg>')
    return "\\n".join(out).replace("\\n","\n")

def main():
    report={"scope":"offline synthetic demonstration, not validated outside fictional cases",
            "datasets":{"scam":model_baselines("scam",SCAM_TRAIN,HELD_OUT["scam"]),
                        "civic":model_baselines("civic",ISSUE_TRAIN,HELD_OUT["civic"])},
            "forecast_cases":{},"limitations":[
              "Only tiny authored synthetic holdouts, not real-world model performance",
              "No time- or geography-separated real-world evaluation",
              "No statistical confidence intervals, bias assessment or live deployment",
              "Class frequency, phrasing and test distribution are artificial"
            ]}
    for slug,values in SYNTH_SERIES.items():
        report["forecast_cases"][slug]=forecast(values,"pm25" if "air-quality" in slug else "illustrative_rainfall")
    OUT.mkdir(exist_ok=True)
    (OUT/"model_baseline_comparison.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    rows=[(name,details["results"]["tfidf_logistic"]["macro_f1"],
                details["results"]["most_frequent_baseline"]["macro_f1"])
          for name,details in report["datasets"].items()]
    (OUT/"model_baseline_chart.svg").write_text(svg_report(rows),encoding="utf8")
    print(json.dumps({"datasets":list(report["datasets"]),"forecast_cases":len(report["forecast_cases"]),
                      "saved":["reports/model_baseline_comparison.json","reports/model_baseline_chart.svg"]},indent=2))

if __name__=="__main__":main()
