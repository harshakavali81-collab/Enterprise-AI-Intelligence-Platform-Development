"""Tiny synthetic corpora only: TF-IDF / logistic-regression demonstration."""
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from urllib.parse import urlsplit
import re
SCAM_TRAIN = [
("claim your reward now verify account password",1),
("urgent bank verify your one time password click",1),
("you won prize send money to redeem",1),
("suspended account enter login credentials now",1),
("pay tax immediately at shortened link",1),
("share otp to confirm transaction",1),
("meeting minutes attached for team review",0),
("please review the sprint planning notes",0),
("lunch next week with our department",0),
("your library books are due next month",0),
("the workshop begins at three this afternoon",0),
("schedule confirmed for the quarterly meeting",0),
]
ISSUE_TRAIN = [
("large pothole on road causing uneven surface","pothole"),
("deep hole in road asphalt and broken pavement","pothole"),
("wheelchair ramp blocked by debris","blocked_access"),
("building accessible entry blocked by parked objects","blocked_access"),
("streetlight lamp is not working at night","streetlight"),
("broken light on roadside pole","streetlight"),
("footpath tiles cracked and raised near curb","footpath"),
("pedestrian sidewalk is badly damaged","footpath"),
]
def classify(text: str, examples: list[tuple]):
    texts,targets = zip(*examples)
    model = Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2))),
                      ("clf",LogisticRegression(max_iter=600,random_state=11))])
    model.fit(texts,targets)
    scores = model.predict_proba([text])[0]
    ix = int(scores.argmax())
    return {"label":str(model.classes_[ix]),"uncalibrated_model_score":round(float(scores[ix]),3),
            "note":"Synthetic training examples; model score is not a calibrated real-world probability"}
def suspicious_link_indicators(text:str):
    found = re.findall(r'https?://[^\s<>"]+',text,flags=re.I)[:10]
    results=[]
    for raw in found:
        try:
            u=urlsplit(raw.rstrip(".,;!"))
            host=(u.hostname or "").lower()
            flags=[]
            if u.scheme=="http":flags.append("unencrypted_scheme")
            if host.startswith("xn--") or ".xn--" in host:flags.append("internationalized_domain")
            if host.replace(".","").isdigit():flags.append("numeric_host")
            if "@" in u.netloc:flags.append("userinfo_in_url")
            if len(host)>50:flags.append("long_hostname")
            results.append({"host":host,"indicators":flags})
        except ValueError:
            results.append({"host":"invalid","indicators":["invalid_url"]})
    return results
