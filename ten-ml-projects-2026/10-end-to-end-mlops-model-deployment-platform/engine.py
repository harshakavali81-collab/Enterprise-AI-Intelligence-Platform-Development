"""Portable, intentionally small ML demonstration engine.
All generated demo data is SYNTHETIC. Results are NOT externally validated.
"""
import json
import hashlib
import time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_fscore_support, mean_absolute_error, mean_squared_error, brier_score_loss, ndcg_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.datasets import load_iris
import joblib

HERE=Path(__file__).resolve().parent
ART=HERE/'artifacts'
FIG=HERE/'docs'/'figures'
MODE='mlops'
SEED=42

def _paths():
    ART.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)

def _save_plot(labels, scores, metric):
    _paths()
    fig,ax=plt.subplots(figsize=(8,4.3))
    bars=ax.bar(labels,scores,color=['#D4AF65','#577E8A','#9B8A78'][:len(labels)])
    for b,v in zip(bars,scores): ax.text(b.get_x()+b.get_width()/2,b.get_height()+.012,f'{v:.3f}',ha='center',fontsize=10)
    ax.set_title(f'{MODE.title()} · Synthetic Holdout {metric}',fontweight='bold')
    ax.set_ylim(0,max(1.05,max(scores)*1.18))
    ax.set_ylabel(metric); ax.grid(axis='y',alpha=.15)
    fig.tight_layout(); fig.savefig(FIG/'evaluation.png',dpi=145); plt.close(fig)

def _class_dataset(mode,n=1300):
    rng=np.random.default_rng(SEED)
    if mode=='fraud':
        amount=np.exp(rng.normal(4,1.35,n)); velocity=rng.poisson(2,n); foreign=rng.binomial(1,.16,n); device=rng.binomial(1,.08,n)
        z=-5.7+0.8*(np.log1p(amount)-4)+.32*velocity+1.35*foreign+1.5*device
        X=np.column_stack([np.log1p(amount),velocity,foreign,device])
        names=['log_amount','velocity','cross_border','new_device']
    elif mode=='churn':
        tenure=rng.uniform(1,72,n); complaints=rng.poisson(.85,n); autopay=rng.binomial(1,.55,n); monthly=rng.uniform(25,145,n)
        z=-1.4-.023*tenure+.72*complaints-.9*autopay+.008*(monthly-75)
        X=np.column_stack([tenure,complaints,autopay,monthly]); names=['tenure_months','complaints_90d','autopay','monthly_cost']
    elif mode=='maintenance':
        temp=rng.normal(65,12,n); vibration=rng.gamma(2.4,.72,n); pressure=rng.normal(100,11,n); hours=rng.uniform(0,7000,n)
        z=-5+.10*(temp-65)+1.1*(vibration-2)+.006*(hours-3500)+.025*abs(pressure-100)
        X=np.column_stack([temp,vibration,pressure,hours]); names=['temp_c','vibration','pressure','hours_used']
    elif mode=='credit':
        income=rng.lognormal(10.5,.55,n); dti=rng.uniform(.03,.89,n); missed=rng.poisson(.55,n); months=rng.uniform(3,90,n)
        z=-3.4+3.8*dti+.75*missed-.017*months-.000008*(income-50000)
        X=np.column_stack([income,dti,missed,months]); names=['annual_income','debt_to_income','missed_payments','loan_age_months']
    else: raise ValueError(mode)
    y=rng.binomial(1,1/(1+np.exp(-np.clip(z,-15,15))))
    return X,y,names

def _image_dataset(mode):
    rng=np.random.default_rng(SEED); X=[]; y=[]; groups=[]; samples=[]
    n_patients=160 if mode=='medical' else 150
    for patient in range(n_patients):
        label=int(rng.random()<.43)
        for rep in range(2):
            im=np.clip(rng.normal(.35,.08,(32,32)),0,1)
            if label:
                if mode=='medical':
                    xx,yy=np.mgrid[:32,:32]; cx,cy=16+rng.integers(-3,4),16+rng.integers(-3,4)
                    im[((xx-cx)**2+(yy-cy)**2)<35]+=.45
                else:
                    row=14+rng.integers(-6,7); im[row:row+2,5:27]+=.5
            im=np.clip(im,0,1)
            # Simple interpretable grayscale features, NOT a CNN.
            feat=[im.mean(),im.std(),np.quantile(im,.9),np.quantile(im,.99),
                  np.abs(np.diff(im,axis=0)).mean(),np.abs(np.diff(im,axis=1)).mean(),
                  im[9:23,9:23].mean(),np.sum(im>.68)/im.size]
            X.append(feat);y.append(label);groups.append(patient)
            if len(samples)<8:samples.append((im,label))
    return np.asarray(X),np.asarray(y),np.asarray(groups),samples

def _classification():
    if MODE in ('vision','medical'):
        X,y,groups,samples=_image_dataset(MODE)
        splitter=GroupShuffleSplit(n_splits=1,test_size=.26,random_state=SEED)
        tr,te=next(splitter.split(X,y,groups))
        assert not (set(groups[tr])&set(groups[te]))
        fig,axes=plt.subplots(2,4,figsize=(8,4.4))
        for ax,(im,label) in zip(axes.flat,samples):
            ax.imshow(im,cmap='gray',vmin=0,vmax=1);ax.set_title('Positive' if label else 'Negative',fontsize=9);ax.axis('off')
        fig.suptitle('SYNTHETIC research images — not real patient/product data')
        fig.tight_layout();_paths();fig.savefig(FIG/'sample_images.png',dpi=130);plt.close(fig)
        names=['mean','std','q90','q99','vertical_edges','horizontal_edges','center_brightness','bright_ratio']
    else:
        X,y,names=_class_dataset(MODE)
        tr,te=train_test_split(np.arange(len(y)),test_size=.25,random_state=SEED,stratify=y)
    models={
      'Logistic Regression':make_pipeline(StandardScaler(),LogisticRegression(max_iter=500,class_weight='balanced',random_state=SEED)),
      'Random Forest':RandomForestClassifier(n_estimators=75,min_samples_leaf=3,class_weight='balanced_subsample',random_state=SEED,n_jobs=-1)
    }
    results={}; best=None; best_score=-1
    for name,model in models.items():
        model.fit(X[tr],y[tr]);pr=model.predict_proba(X[te])[:,1]
        ap=float(average_precision_score(y[te],pr));auc=float(roc_auc_score(y[te],pr))
        precision,recall,f1,_=precision_recall_fscore_support(y[te],pr>=.5,average='binary',zero_division=0)
        results[name]={'pr_auc':round(ap,4),'roc_auc':round(auc,4),'precision':round(float(precision),4),'recall':round(float(recall),4),'f1':round(float(f1),4),'brier':round(float(brier_score_loss(y[te],pr)),4)}
        if ap>best_score: best_score=ap;best=(name,model)
    _save_plot(list(results),[x['pr_auc'] for x in results.values()],'PR-AUC')
    _paths();joblib.dump(best[1],ART/'model.joblib')
    return {'mode':MODE,'dataset':'synthetic','records':len(X),'positive_rate':round(float(y.mean()),4),'features':names,'split':'group-by-patient' if MODE=='medical' else ('group-by-source' if MODE=='vision' else 'stratified holdout'),'models':results,'selected':best[0],'limitation':'Not validated on any real-world dataset. Research/demo use only.'}

def _retail():
    rng=np.random.default_rng(SEED);d=np.arange(440);promo=rng.binomial(1,.20,len(d))
    sales=np.maximum(0,32+9*np.sin(2*np.pi*d/7)+.04*d+12*promo+rng.normal(0,5,len(d))).round()
    # Features use lagged observations only; no future sales leakage.
    x=np.array([[sales[i-7],np.mean(sales[i-7:i]),int(i%7),promo[i],i] for i in range(14,len(d))]);y=sales[14:]
    tr=np.arange(len(y)-90);te=np.arange(len(y)-90,len(y))
    baseline=x[te,0]; model=RandomForestRegressor(n_estimators=95,min_samples_leaf=3,random_state=SEED,n_jobs=-1)
    model.fit(x[tr],y[tr]);pr=model.predict(x[te]);
    metrics={name:{'mae':round(float(mean_absolute_error(y[te],yp)),3),'rmse':round(float(np.sqrt(mean_squared_error(y[te],yp))),3),'wape':round(float(np.abs(y[te]-yp).sum()/max(1,y[te].sum())),4)} for name,yp in [('Seasonal naive',baseline),('Random Forest',pr)]}
    fig,ax=plt.subplots(figsize=(9,4));ax.plot(y[te][-45:],label='Actual',linewidth=2);ax.plot(pr[-45:],label='Forecast',alpha=.85);ax.legend();ax.set_title('Synthetic retail daily demand: holdout');ax.set_ylabel('Units');fig.tight_layout();_paths();fig.savefig(FIG/'forecast.png',dpi=150);plt.close(fig)
    _save_plot(list(metrics),[1-z['wape'] for z in metrics.values()],'1 − WAPE (display only)')
    joblib.dump(model,ART/'model.joblib')
    lead_days=7;safety=int(np.ceil(1.65*np.std(sales[-90:])*np.sqrt(lead_days)))
    return {'mode':MODE,'dataset':'synthetic','features':['lag7_sales','last7_mean','day_of_week','promo','day_index'],'split':'chronological last 90 days','models':metrics,'reorder_point_units':int(np.ceil(sales[-30:].mean()*lead_days+safety)),'safety_stock_units':safety,'note':'Reorder simulation assumes independent demand variation; no stock constraints, sales censoring or supplier data.'}

def _recommend():
    rng=np.random.default_rng(SEED);nu,ni=65,90; u=rng.normal(size=(nu,5));v=rng.normal(size=(ni,5));score=u@v.T+rng.normal(scale=.55,size=(nu,ni));
    train={};test={}
    for person in range(nu):
        order=np.argsort(score[person])[::-1][:16];train[person]=list(map(int,order[:12]));test[person]=list(map(int,order[12:16]))
    mat=np.zeros((nu,ni));
    for user,ids in train.items():mat[user,ids]=1
    popular=mat.sum(axis=0);sim=cosine_similarity(mat.T);np.fill_diagonal(sim,0)
    result={}
    for name in ['Popularity','Collaborative cosine']:
        recalls=[];ndcgs=[]
        for user in range(nu):
            vec=popular.astype(float).copy() if name=='Popularity' else sim[:,train[user]].sum(axis=1)
            vec[train[user]]=-1e9;top=np.argsort(vec)[-5:][::-1]
            target=np.zeros(ni);target[test[user]]=1
            recalls.append(len(set(top)&set(test[user]))/len(test[user]))
            ndcgs.append(float(ndcg_score(target.reshape(1,-1),vec.reshape(1,-1),k=5)))
        result[name]={'recall_at_5':round(float(np.mean(recalls)),4),'ndcg_at_5':round(float(np.mean(ndcgs)),4)}
    _save_plot(list(result),[v['recall_at_5'] for v in result.values()],'Recall@5')
    _paths();joblib.dump({'matrix':mat,'popularity':popular,'similarity':sim},ART/'model.joblib')
    return {'mode':MODE,'dataset':'synthetic latent-preference simulator','users':nu,'items':ni,'split':'12 observed and 4 held-out positive interactions/user; no timestamps','models':result,'note':'Offline synthetic evaluation; not evidence of performance for real users.'}

KB=[
 ('fraud','Fraud alerts need human review.','धोखाधड़ी अलर्ट की मानव समीक्षा जरूरी है।','మోసం హెచ్చరికలను మనుషులు సమీక్షించాలి.'),
 ('inventory','Reorder points include lead-time demand and safety stock.','पुनः ऑर्डर बिंदुओं में लीड टाइम की मांग और सुरक्षा स्टॉक शामिल हैं।','మళ్లీ ఆర్డర్ చేసే స్థాయిలో సరఫరా సమయం మరియు భద్రతా నిల్వ ఉన్నాయి.'),
 ('churn','A churn score does not prove a discount will help.','चर्न स्कोर से यह साबित नहीं होता कि छूट मदद करेगी।','చర్న్ స్కోర్ వల్ల రాయితీ ఉపయోగపడుతుందని నిరూపితం కాదు.'),
 ('medical','Synthetic medical images cannot support diagnosis.','कृत्रिम चिकित्सा चित्रों से निदान नहीं हो सकता।','కృత్రిమ వైద్య చిత్రాలు రోగ నిర్ధారణకు పనికిరావు.'),
 ('mlops','A production model needs reproducible tests and monitoring.','प्रोडक्शन मॉडल को पुनरुत्पादित परीक्षण और निगरानी चाहिए।','ప్రొడక్షన్ మోడల్‌కు పునరుత్పాదక పరీక్షలు మరియు పర్యవేక్షణ అవసరం.'),
 ('search','Source citations must point to retrieved evidence.','स्रोत उद्धरण प्राप्त प्रमाण से जुड़े होने चाहिए।','మూల సూచనలు తిరిగి పొందిన ఆధారాలను చూపాలి.'),
]

def _search():
    docs=[];queries=[]
    for topic,en,hi,te in KB:
        docs.append({'id':f'kb:{topic}','title':topic,'text':en+' '+hi+' '+te})
        for q in (en,hi,te):queries.append((q,f'kb:{topic}'))
    vectorizer=TfidfVectorizer(analyzer='char',ngram_range=(2,5));matrix=vectorizer.fit_transform([d['text'] for d in docs]);
    ranks=[]
    for q,truth in queries:
        similarities=cosine_similarity(vectorizer.transform([q]),matrix).ravel();order=np.argsort(similarities)[::-1][:3];ranks.append(int(any(docs[i]['id']==truth for i in order)))
    _paths();joblib.dump({'vectorizer':vectorizer,'matrix':matrix,'documents':docs},ART/'model.joblib')
    _save_plot(['EN/HI/TE self-query'],[float(np.mean(ranks))],'Recall@3')
    return {'mode':MODE,'dataset':'6 original tri-lingual synthetic reference passages','num_documents':len(docs),'queries':len(queries),'recall_at_3':round(float(np.mean(ranks)),4),'approach':'TF-IDF character ngrams over parallel-language passages; no embeddings or LLM','note':'Toy corpus; near-identical query text is an intentionally easy retrieval benchmark. Not robust cross-language retrieval.'}

def _mlops():
    iris=load_iris(); X=iris.data;y=iris.target
    tr,te=train_test_split(np.arange(len(y)),test_size=.28,random_state=SEED,stratify=y)
    models={'Logistic Regression':make_pipeline(StandardScaler(),LogisticRegression(max_iter=500,random_state=SEED)),'Random Forest':RandomForestClassifier(n_estimators=80,random_state=SEED)}
    scores={}
    for name,model in models.items():
        model.fit(X[tr],y[tr]);scores[name]=round(float((model.predict(X[te])==y[te]).mean()),4)
    winner=max(scores,key=scores.get)
    _paths();joblib.dump(models[winner],ART/'model.joblib');ref={'mean':X[tr].mean(axis=0).tolist(),'std':np.maximum(X[tr].std(axis=0),1e-8).tolist()};(ART/'reference.json').write_text(json.dumps(ref,indent=2))
    _save_plot(list(scores),list(scores.values()),'Accuracy')
    return {'mode':MODE,'dataset':'scikit-learn Iris (bundled public sample)','split':'stratified 28% holdout','models':scores,'selected':winner,'release_gate_pass':bool(scores[winner]>=.8),'reference_stats':'artifacts/reference.json','note':'Locally reproducible release demo; no actual cloud deployment, MLflow registry or automated retraining.'}

def drift_alert(X,reference_path=ART/'reference.json',threshold=2.5):
    ref=json.loads(Path(reference_path).read_text());x=np.asarray(X,dtype=float)
    if x.ndim==1:x=x.reshape(1,-1)
    if x.shape[1]!=len(ref['mean']):raise ValueError('Wrong feature count')
    z=np.abs((x.mean(axis=0)-np.array(ref['mean']))/np.array(ref['std']))
    return {'drift_alert':bool(np.max(z)>threshold),'max_mean_shift_std':float(np.max(z)),'note':'Heuristic mean-shift alert, not a formal drift significance test.'}

def train():
    start=time.perf_counter()
    if MODE=='retail': result=_retail()
    elif MODE=='recommend': result=_recommend()
    elif MODE=='search': result=_search()
    elif MODE=='mlops': result=_mlops()
    else: result=_classification()
    result['seed']=SEED;result['execution_seconds']=round(time.perf_counter()-start,2)
    content=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)
    (ART/'metrics.json').write_text(content+'\n',encoding='utf-8')
    digest=hashlib.sha256((ART/'model.joblib').read_bytes()).hexdigest()[:14]
    (ART/'model_manifest.json').write_text(json.dumps({'mode':MODE,'model_sha256_short':digest,'data_provenance':result['dataset'],'seed':SEED},indent=2))
    return result

def infer(features):
    model=joblib.load(ART/'model.joblib');a=np.asarray(features,dtype=float).reshape(1,-1)
    if MODE in ('search','recommend'): raise ValueError('Use retrieve() or recommend() instead')
    if MODE=='mlops':return {'predicted_class':int(model.predict(a)[0]),'probabilities':model.predict_proba(a)[0].tolist()}
    if MODE=='retail':return {'demand_units':round(float(max(0,model.predict(a)[0])),2)}
    return {'positive_probability':round(float(model.predict_proba(a)[0,1]),5),'decision_threshold':.5,'review_recommended':bool(model.predict_proba(a)[0,1]>=.5)}

def retrieve(question,k=3):
    if MODE!='search':raise ValueError('Not a search project')
    data=joblib.load(ART/'model.joblib');scores=cosine_similarity(data['vectorizer'].transform([question]),data['matrix']).ravel();order=np.argsort(scores)[::-1][:k]
    return [{'source_id':data['documents'][int(i)]['id'],'evidence':data['documents'][int(i)]['text'],'score':round(float(scores[int(i)]),4)} for i in order if scores[int(i)]>0]

def recommend(user_id,k=5):
    if MODE!='recommend':raise ValueError('Not a recommender project')
    m=joblib.load(ART/'model.joblib');arr=m['matrix'];user=int(user_id)
    if not 0<=user<arr.shape[0]:raise ValueError('Unknown user: 0 to '+str(arr.shape[0]-1))
    seen=np.where(arr[user]>0)[0].tolist();scores=m['similarity'][:,seen].sum(axis=1);scores[seen]=-1e9
    return {'user_id':user,'item_ids':np.argsort(scores)[-k:][::-1].astype(int).tolist(),'source':'synthetic collaborative similarity'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('action',choices=['train','predict','search','recommend','drift']);p.add_argument('--features',default='');p.add_argument('--query',default='');p.add_argument('--user-id',type=int,default=0);args=p.parse_args()
    if args.action=='train':out=train()
    elif args.action=='predict':out=infer([float(x) for x in args.features.split(',')])
    elif args.action=='search':out=retrieve(args.query)
    elif args.action=='recommend':out=recommend(args.user_id)
    else:out=drift_alert([float(x) for x in args.features.split(',')])
    print(json.dumps(out,indent=2,ensure_ascii=False))
