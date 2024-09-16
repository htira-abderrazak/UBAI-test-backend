from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
import spacy

nlp = spacy.load("en_core_web_md")
class Annotate(APIView):
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text', None)
        
        labels = request.query_params.getlist('labels', [])
        
        if text is None:
            return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(labels, list):
            return Response({"error": "Labels must be a list"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        annotations = annotate_text(text, labels)
        response={"document": text, "annotations": annotations}
        
        return Response( response)


#this task must excute in background with celery for more performence
def annotate_text(text, labels, threshold=0.5):
    doc = nlp(text)
    label_tokens = {label: nlp(label)[0] for label in labels}
    annotations = []

    entities_and_noun_chunks = list(doc.ents) + list(doc.noun_chunks)

    for ent in entities_and_noun_chunks:
        for label, label_token in label_tokens.items():
            if label_token.similarity(ent) > threshold:
                annotations.append({
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "label": label,
                    "text": ent.text
                })

    return annotations