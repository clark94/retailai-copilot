from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
ROOT=Path(__file__).resolve().parents[1]/'rag_docs'

def retrieve(question,k=3):
    docs=[(p.name,p.read_text(encoding='utf-8')) for p in sorted(ROOT.glob('*.txt'))]
    if not docs:return []
    vectorizer=TfidfVectorizer(ngram_range=(1,2),strip_accents='unicode')
    matrix=vectorizer.fit_transform([text for _,text in docs]+[question])
    scores=cosine_similarity(matrix[-1],matrix[:-1]).ravel()
    return [{'source':docs[i][0],'extrait':docs[i][1][:1300],'score':round(float(scores[i]),3)}
            for i in scores.argsort()[::-1][:k] if scores[i]>=0.04]

def answer(question):
    hits=retrieve(question)
    if not hits:return {'answer':'Je ne trouve pas de source documentaire suffisamment pertinente.','sources':[],'mode':'retrieval-only'}
    # Sans clé LLM, ne prétend pas générer une réponse: renvoie un extrait traçable.
    import os
    if os.getenv('OPENAI_API_KEY'):
        try:
            from openai import OpenAI
            client=OpenAI(api_key=os.environ['OPENAI_API_KEY'],base_url=os.getenv('OPENAI_BASE_URL','https://api.openai.com/v1'))
            context='\n\n'.join(f"SOURCE {h['source']}: {h['extrait']}" for h in hits)
            res=client.chat.completions.create(model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),messages=[
              {'role':'system','content':'Réponds en français UNIQUEMENT à partir du contexte. Cite les fichiers. Si le contexte est insuffisant, dis-le. Les documents fictifs ne sont pas des règles officielles.'},
              {'role':'user','content':f'Contexte:\n{context}\n\nQuestion: {question}'}],temperature=0)
            return {'answer':res.choices[0].message.content,'sources':hits,'mode':'llm-rag'}
        except Exception as exc:
            return {'answer':f'LLM indisponible ({type(exc).__name__}). Voici le passage documentaire trouvé : '+hits[0]['extrait'],'sources':hits,'mode':'retrieval-only'}
    return {'answer':'Extrait de '+hits[0]['source']+' : '+hits[0]['extrait'],'sources':hits,'mode':'retrieval-only'}
