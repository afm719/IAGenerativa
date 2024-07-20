def generate_embeddings(chunks):

    vectors = []
    for i, chunk in enumerate(chunks):
      response = client.embeddings.create(
      input=chunk,
      model="text-embedding-ada-002"
      )

      vector_dict = {
            "id": f"{i + 1}",  # Asignar letras del alfabeto como identificadores
            "values": response.data[0].embedding,
            "metadata": {"text": chunk}  # Puedes ajustar esto según tus datos reales
        }
      vectors.append(vector_dict)

    return vectors
