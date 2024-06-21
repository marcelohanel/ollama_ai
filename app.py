import ollama
import pandas as pd

pergunta = ""
df = pd.read_excel("Vendas.xlsx")
df = df.drop(["Código Venda", "Quantidade", "Valor Unitário"], axis=1)
df_text = df.to_string(index=False)

print(df_text)
print()
print()


while pergunta != "sair": 

    pergunta = input("Digite sua pergunta: ")
    if pergunta == "sair":
        break

    response = ollama.chat(
        model="gemma", 
        messages=[
            { "role": "system", "content": "Seja sempre objetivo nas respostas" },
            { "role": "system", "content": "Responda sempre em portugues do Brasil" },
            { "role": "system", "content": "Mostre sempre o valor calculado" },
            { "role": "system", "content": "Nunca mostre o detalhamento do cálculo" },
            { "role": "user", "content": f"{df_text}" },
            { "role": "user", "content": f"{pergunta}" },
        ],
        stream=True,
    )

    for chunk in response:
        print(chunk["message"]["content"], end="", flush=True)

    print()
    print()