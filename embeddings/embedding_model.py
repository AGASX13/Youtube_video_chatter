"""
Ollama embedding model integration.
"""

from typing import Optional
from langchain_community.embeddings import OllamaEmbeddings

from app.config import Config
from utils.helpers import get_logger

logger = get_logger(__name__)


class EmbeddingModel:
    """Wrapper for Ollama embeddings."""

    def __init__(
        self,
        model_name: str = Config.EMBEDDING_MODEL,
        ollama_base_url: str = Config.OLLAMA_BASE_URL,
    ):
        """
        Initialize embedding model.

        Args:
            model_name: Name of the Ollama embedding model
            ollama_base_url: Base URL for Ollama service
        """
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url

        try:
            self.embeddings = OllamaEmbeddings(
                model=model_name,
                base_url=ollama_base_url,
            )
            logger.info(f"Initialized Ollama embeddings: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama embeddings: {str(e)}")
            raise

    def embed_query(self, query: str) -> list[float]:
        """
        Embed a single query.

        Args:
            query: Query text to embed

        Returns:
            Embedding vector
        """
        try:
            return self.embeddings.embed_query(query)
        except Exception as e:
            logger.error(f"Failed to embed query: {str(e)}")
            raise

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """
        Embed multiple documents.

        Args:
            documents: List of document texts to embed

        Returns:
            List of embedding vectors
        """
        if not documents:
            logger.warning("Empty documents list provided")
            return []

        try:
            embeddings = self.embeddings.embed_documents(documents)
            logger.info(f"Embedded {len(documents)} documents")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to embed documents: {str(e)}")
            raise

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings.

        Returns:
            Embedding dimension
        """
        try:
            test_embedding = self.embed_query("test")
            dimension = len(test_embedding)
            logger.info(f"Embedding dimension: {dimension}")
            return dimension
        except Exception as e:
            logger.error(f"Failed to get embedding dimension: {str(e)}")
            raise


if __name__ == "__main__":
    try:
        embedder = EmbeddingModel()

        # Test embedding
        test_text = "This is a test query for embedding"
        embedding = embedder.embed_query(test_text)
        print(f"Query embedding dimension: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")

        # Test batch embedding
        test_docs = ["Document one", "Document two", "Document three"]
        batch_embeddings = embedder.embed_documents(test_docs)
        print(f"Batch embedded {len(batch_embeddings)} documents")

    except Exception as e:
        print(f"Error: {str(e)}")
