- 텍스트 데이터를 분류하는 모델 study 
- 아래 3가지 예시는 공통적으로 '품모명'을 활용하여 '카테고리'를 분류하는 예제코드이다.
  

### 1. Logistic Regression (with TF-IDF vectorization)
(기본적인 모델이지만 빠르고 해석이 쉬움)

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(train_df['품목명'], train_df['카테고리'], test_size=0.2, random_state=42)

# 파이프라인 생성: 텍스트 전처리 + 로지스틱 회귀
model = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
    ('clf', LogisticRegression(max_iter=1000))
])

# 학습
model.fit(X_train, y_train)

# 평가
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

```

- TfidfVectorizer: 텍스트를 수치화하는 대표적인 방법으로 단어의 중요도를 반영.
- LogisticRegression: 다중 클래스 분류에도 적합하며 속도가 빠름.
- Pipeline: 전처리와 모델을 한 번에 처리할 수 있도록 구성.

### 2. Random Forest (with CountVectorizer)
(비선형 패턴까지 잘 잡고, 해석 가능한 트리 기반 모델)
```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(train_df['품목명'], train_df['카테고리'], test_size=0.2, random_state=42)

# 파이프라인 생성: BoW + 랜덤포레스트
model = Pipeline([
    ('vect', CountVectorizer(ngram_range=(1, 2), max_features=5000)),
    ('clf', RandomForestClassifier(n_estimators=200, random_state=42))
])

# 학습
model.fit(X_train, y_train)

# 평가
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

```

- CountVectorizer: 단어 빈도를 기반으로 특성 벡터를 생성.
- RandomForestClassifier: 앙상블 방식으로 정확도가 높고 과적합에도 강함.
- n_estimators=200: 결정 트리 개수, 더 늘리면 성능 개선 가능.

### 3. BERT 기반 분류 모델 (transformers 사용)
(문맥 이해가 필요한 경우 강력한 성능, 특히 유사 품목명이 많은 경우 추천)
```python
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch

# 라벨 인코딩
label2id = {label: idx for idx, label in enumerate(train_df['카테고리'].unique())}
train_df['label'] = train_df['카테고리'].map(label2id)

# Huggingface Dataset으로 변환
dataset = Dataset.from_pandas(train_df[['품목명', 'label']])

# 토크나이저 및 전처리
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def preprocess(example):
    return tokenizer(example['품목명'], truncation=True, padding='max_length', max_length=64)

dataset = dataset.map(preprocess)

# 모델 로드
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label2id))

# 트레이닝 설정
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='no',
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir='./logs',
    logging_steps=10,
)

# Trainer 객체 생성 및 학습
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()

```
- transformers 라이브러리는 사전 학습된 언어모델을 활용.
- BertTokenizer: 문장을 WordPiece로 토큰화하여 BERT에 입력.
- BertForSequenceClassification: 텍스트 분류 전용 BERT 아키텍처.
- Trainer: 모델 학습 루프를 자동화해주는 툴.
