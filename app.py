import ollama
import pandas as pd
import json

pergunta = ""
system = ""
usuario = ""

df = pd.read_excel("kpi013d.xlsx")
df['dtMovto'] = df['dtMovto'].dt.strftime('%d-%m-%Y') 
df['anoMesDiaMovto'] = df['anoMesDiaMovto'].dt.strftime('%Y-%m-%d')  
df['anoMesMovto'] = df['anoMesMovto'].dt.strftime('%Y-%m')  
df['mesAnoMovto'] = df['mesAnoMovto'].dt.strftime('%m-%Y')  

data = df.to_dict(orient='records')
with open('kpi013d.json', 'w') as f:
    json.dump(data, f, indent=3)

with open('kpi013d.json', 'r') as f:
    df_text = f.read()

def chat(pergunta="/n"):
    messages = []
    usuario_mensagem = usuario + pergunta
    messages.append({ "role": "system", "content": system })
    messages.append({ "role": "user", "content": usuario_mensagem })

    response = ollama.chat(
        model="mistral:latest", 
        messages=messages,
        stream=True,
        options= {
            "top_k": 3,
            "top_p": 0.3,
            "temperature": 0.0,
        }
    ) 

    for chunk in response:
        print(chunk["message"]["content"], end="", flush=True)  

    print()
    print()

system = "Se comporte como um analista de dados /n"
system += "Mostre respostar objetivas e sucintas /n"
system += "Responda sempre em portugues do Brasil /n"
system += "Nunca mostre exemplos de código /n"
system += "Seja sempre objetivo e sucinto nas respostas /n"

usuario = df_text + "/n"
usuario += "Isto é um arquivo JSON para análise /n"

chat("Me mostre colunas que possui este JSON com uma explicação de cada uma")

while pergunta != "sair": 

    pergunta = input("Digite sua pergunta: ")
    if pergunta == "sair":
        break

    chat(pergunta)