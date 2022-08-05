from sentence_transformers import SentenceTransformer

ckpt = "all-MiniLM-L6-v2"
model = SentenceTransformer(ckpt)
model.save("key_ext_small")