import spacy
from collections import Counter


class NER():
    def __init__(self,text):
        self.text = text

    def load_model(self):
        import en_core_web_sm
        ner_model = en_core_web_sm.load()
        return ner_model
    
    def form_doc(self):
        ner_model = self.load_model()
        self.doc = ner_model(self.text)
        return self.doc

    def get_entities(self):
        doc = self.form_doc()
        entities = [ent for ent in doc.ents]
        # Consider only person, location, organization entities
        entities = [ent for ent in entities if ent.label_ in ("PERSON", "LOC", "ORG", "GPE", "FAC", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")]
        return entities


    

