from sentence_transformers import SentenceTransformer, util

modelo_semantico = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def semantica(prompt, base):
    temas = [item["tema"] for item in base]
    embeddings_base = modelo_semantico.encode(temas, convert_to_tensor=True)
    embedding_prompt = modelo_semantico.encode(prompt, convert_to_tensor=True)

    similaridades = util.cos_sim(embedding_prompt, embeddings_base)[0]
    indice_mais_proximo = similaridades.argmax().item()
    maior_score = similaridades[indice_mais_proximo].item()
    print(f"Prompt: {prompt}")
    print(f"Tema detectado: {temas[indice_mais_proximo]}")
    print(f"Score: {maior_score}")

    if maior_score > 0.4: 
        return temas[indice_mais_proximo]
    return None
