from config.llm_config import Config
import os
import openai
import constants
from config.db_config import Db_config

db = Db_config()

class investment_advisor(Config):

    SYSTEM_PROMPT = """
    You are an "expert investment advisor". You should be able to advice client based on the input data provided 
    on topics like:
        - what stocks to buy?
        - How much to invest?
        - For how long they should invest to get good returns.

    INSTRUCTIONS:
    Use the following pieces of context to answer the user question.
    You must only use the facts from the context to answer. 
    Never hallucinate.
    Be professional & polite in your responses. 
    If the answer is NOT in the context, respond with: "I don't have information about that in the provided documents."
    If the answer cannot be found in the context, say that you don't have enough information to answer the question and provide any relevant facts found in the context.

    Context:
    {context}

"""

    def __init__(self):
        super().__init__()
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
        self.OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

    def investment_advice(self, user_input: str) -> dict:
        user_query_embedding = self.generarte_query_embeddings(user_input=user_input)
        context = self.similarity_search(user_query_embedding)
        return self.chain_prompt(self.SYSTEM_PROMPT.format(context=context), 
                                 user_input, 
                                 constants.AGENT_STATE_INVESTMENT_ADVISOR)


    def generarte_query_embeddings(self, user_input: str):
        client = openai.OpenAI(api_key=self.OPEN_API_KEY)
        response = client.embeddings.create(model=self.EMBEDDING_MODEL, 
                                    input=user_input)
        
        return response.data[0].embedding
    
    def similarity_search(self, query_embedding, k=3):
        conn = db.get_db_connection()
        context_chunks = []

        query = """
        SELECT content, 1 - (embedding <=> '{query_embedding}') as similarity FROM documents ORDER BY similarity DESC LIMIT {k}
        """.format(query_embedding=query_embedding, k=12)
        
        with conn.cursor() as cur:
            # The <=> operator computes the distance. We order by this distance (closest first).
            cur.execute(
                query
            )

            result = cur.fetchall()
            for row in result:
                context_chunks.append(row[0])
        
        conn.close()
        return context_chunks



