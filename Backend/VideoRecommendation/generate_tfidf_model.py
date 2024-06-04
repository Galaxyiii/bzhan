import pymongo
from tqdm import tqdm
import jieba
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim import corpora
import numpy as np
import os

# MongoDB configuration
M_HOST = "localhost"  # Database host
M_PORT = 27017  # Database port
M_USER = None  # Set to None if no user
M_PASSWORD = None  # Set to None if no password

# Connect to MongoDB
client = pymongo.MongoClient(host=M_HOST, port=M_PORT, username=M_USER, password=M_PASSWORD)
mydb = client["bzhan"]
mycol = mydb["bilibili"]
cursor = mycol.find({}, {"title": 1, "id": 1, "description": 1}).limit(1500000)
data = [(x["id"], list(jieba.cut(x["title"]))) for x in tqdm(cursor)]

aids = [x[0] for x in data]
texts = [x[1] for x in data]

# Create data directory if it does not exist
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# Build dictionary and corpus
dictionary = Dictionary(texts)
num_features = len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]

# Create TF-IDF model
tfidf = TfidfModel(corpus)
tf_texts = tfidf[corpus]

# Calculate similarity matrix
sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)

# Save model, dictionary, corpus, and aid
model_path = os.path.join(data_dir, "VideoTitle-TFIDF.model")
dictionary_path = os.path.join(data_dir, "VideoTitle-Dic.dic")
corpus_path = os.path.join(data_dir, "VideoTitle-Corpus.corpus")
aid_path = os.path.join(data_dir, "VideoTitle-Aid.txt")

print(f"Saving model to {model_path}")
tfidf.save(model_path)

print(f"Saving dictionary to {dictionary_path}")
dictionary.save(dictionary_path)

print(f"Saving corpus to {corpus_path}")
corpora.MmCorpus.serialize(corpus_path, corpus)

print(f"Saving aids to {aid_path}")
with open(aid_path, "w") as fin:
    fin.writelines([str(aid) + "\n" for aid in aids])

print("All files saved successfully.")
