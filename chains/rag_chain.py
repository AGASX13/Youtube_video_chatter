"""
RAG Chain implementation using LangChain Expression Language (LCEL).
"""

from typing import Optional
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from app.config import Config
from retrieval.retriever import DocumentRetriever
from vectorstore.faiss_store import FAISSVectorStore
from utils.helpers import get_logger, format_documents

logger = get_logger(__name__)


class RAGChain:
    """RAG chain combining retriever and LLM."""

    def __init__(
        self,
        llm_model: str = Config.LLM_MODEL,
        ollama_base_url: str = Config.OLLAMA_BASE_URL,
        retriever: Optional[DocumentRetriever] = None,
        temperature: float = 0.7,
    ):
        """
        Initialize RAG chain.

        Args:
            llm_model: Name of Ollama model to use
            ollama_base_url: Base URL for Ollama service
            retriever: DocumentRetriever instance
            temperature: Model temperature (0-1)
        """
        self.llm_model = llm_model
        self.temperature = temperature

        # Initialize LLM
        try:
            self.llm = ChatOllama(
                model=llm_model,
                base_url=ollama_base_url,
                temperature=temperature,
                top_k=10,
                top_p=0.9,
            )
            logger.info(f"Initialized ChatOllama with model: {llm_model}")
        except Exception as e:
            logger.error(f"Failed to initialize ChatOllama: {str(e)}")
            raise

        # Initialize retriever
        if retriever is None:
            retriever = DocumentRetriever()

        self.retriever = retriever

        # Build chain
        self.chain = self._build_chain()

    def _build_chain(self):
        """Build the RAG chain using LCEL."""
        # Define system and human prompts
        system_prompt_text = """You are a helpful assistant answering questions based on provided context.

IMPORTANT RULES:
1. Answer ONLY based on the provided context
2. If the answer is not in the context, respond with: "I don't have information about that in the provided context"
3. Always cite which part of the context you're using
4. Be concise and clear
5. If the context is unclear, ask for clarification

Context:
{context}"""

        human_prompt_text = "{question}"

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt_text),
                HumanMessagePromptTemplate.from_template(human_prompt_text),
            ]
        )

        # Build chain using LCEL
        rag_chain = (
            RunnableParallel(
                context=(self.retriever.retrieve | format_documents),
                question=RunnablePassthrough(),
            )
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain

    def invoke(self, question: str) -> str:
        """
        Get answer for a question.

        Args:
            question: User question

        Returns:
            Answer from the model
        """
        try:
            logger.info(f"Processing question: {question}")
            answer = self.chain.invoke({"question": question})
            logger.info("Successfully generated answer")
            return answer
        except Exception as e:
            logger.error(f"Failed to generate answer: {str(e)}")
            return f"Error generating answer: {str(e)}"

    def invoke_with_documents(self, question: str) -> dict:
        """
        Get answer and retrieve context documents.

        Args:
            question: User question

        Returns:
            Dictionary with answer and documents
        """
        try:
            logger.info(f"Processing question with context: {question}")

            # Get documents
            documents = self.retriever.retrieve(question)

            # Get answer
            answer = self.chain.invoke({"question": question})

            return {
                "question": question,
                "answer": answer,
                "documents": documents,
                "num_documents": len(documents),
            }
        except Exception as e:
            logger.error(f"Failed to process question: {str(e)}")
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "documents": [],
                "num_documents": 0,
            }

    def set_temperature(self, temperature: float) -> None:
        """
        Set model temperature.

        Args:
            temperature: Temperature value (0-1)
        """
        if not (0 <= temperature <= 1):
            raise ValueError("Temperature must be between 0 and 1")

        self.temperature = temperature
        self.llm.temperature = temperature
        self.chain = self._build_chain()
        logger.info(f"Set temperature to {temperature}")

    def set_top_k(self, top_k: int) -> None:
        """
        Set retriever top_k.

        Args:
            top_k: Number of documents to retrieve
        """
        self.retriever.set_top_k(top_k)
        logger.info(f"Set retriever top_k to {top_k}")


if __name__ == "__main__":
    try:
        from embeddings.embedding_model import EmbeddingModel

        embedding_model = EmbeddingModel()
        vectorstore = FAISSVectorStore(embedding_model=embedding_model)

        # Create test index
        test_docs = [
            "Python is a high-level programming language known for its simplicity.",
            "Machine learning enables computers to learn from data without being explicitly programmed.",
            "Natural language processing allows computers to understand human language.",
        ]
        vectorstore.create_index(test_docs)

        # Test RAG chain
        retriever = DocumentRetriever(vectorstore=vectorstore, top_k=2)
        rag_chain = RAGChain(retriever=retriever)

        # Ask a question
        question = "What is Python?"
        result = rag_chain.invoke_with_documents(question)

        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print(f"Documents used: {result['num_documents']}")

    except Exception as e:
        print(f"Error: {str(e)}")
