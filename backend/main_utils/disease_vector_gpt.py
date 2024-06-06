import pandas as pd
import chromadb
import googletrans


def vector_collection(text):
    df = pd.read_csv('D:/연구실/수업/2-1/융프/웹사이트/simnursebe-main/main_utils/medical_data.csv')
    
    client = chromadb.PersistentClient(path='./')
    
    collection = client.get_or_create_collection(
    name="medical_data",
    metadata={"hnsw:space" : "cosine"}
    )
    
    ids = []
    doc_meta = []
    documents = []
    
    for idx in range(len(df)):
        item = df.iloc[idx]
        id = item['용어'].lower().replace(' ', '')
        if id in ids:
            continue
        document = f"{item['용어']}: {item[' 내용']}"
        meta = {
            "rating" : item['용어']
        }
    
        ids.append(id)
        doc_meta.append(meta)
        documents.append(document)
            
    collection.add(
        documents = documents,
        metadatas = doc_meta,
        ids = ids
    )

        
    translator = googletrans.Translator()

    inStr = text

    outStr = translator.translate(inStr, dest = 'en', src='auto')
    #srchres= vector_collection(text)
    
    vector_res = collection.query(
    query_texts=[outStr.text],
    n_results=3,
    )
    srchres = []
    
    for v in vector_res['documents'][0]:
        item = v.split(':')
        item_content = item[2].strip().replace(u'\xa0',u' ')
        srchres.append({
            "title" : item[0].strip(),
            "content" : item_content
        })
        
    print(srchres)
    return srchres