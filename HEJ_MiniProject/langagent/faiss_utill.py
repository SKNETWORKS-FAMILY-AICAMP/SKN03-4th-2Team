
import logging
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local('./langagent/faiss', embedding_function, allow_dangerous_deserialization=True)
logging.info("FAISS vector store loaded from './langagent/faiss'")

def query_subwaystations_recommendations(user_input):
    try:
        logging.info(f"Starting query search: {user_input}")

        retriever = vectorstore.as_retriever(search_type="similarity")
        search_results = retriever.invoke(user_input)

        logging.info("Query search completed")

        cleaned_results = []
        for doc in search_results:
            content = doc.page_content.strip()
            metadata = doc.metadata 
            cleaned_results.append({
                "content": content,
                "metadata": metadata 
            })
        return cleaned_results

    except Exception as e:
        logging.error(f"Error during query search: {e}")
        return []