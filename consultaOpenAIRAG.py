def get_answer(question):
    # Hacer el embedding de la pregunta
    response = client.embeddings.create(input=question, model="text-embedding-ada-002")
    embeddings_question = response.data[0].embedding

    # Consulta a la base de datos Pinecone
    potenciales_respuestas = index.query(vector=embeddings_question, top_k=3, include_metadata=True)

    # Formatear las respuestas potenciales para el prompt
    pot_respuestas_formatted = ""
    for pot_resp in potenciales_respuestas['matches']:
        pot_respuestas_formatted += "\n " + pot_resp['metadata']['text'][0]

    # Crear el prompt
    prompt = f"""
    En base al siguiente contexto, contesta mi pregunta.
    contexto: {pot_respuestas_formatted}
    Mi pregunta es: {question}
    """

    # Obtener la respuesta de GPT-3.5 Turbo
    gpt_response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "#####"},
        {"role": "user", "content": prompt}
    ]
    )

    return gpt_response.choices[0].message.content
