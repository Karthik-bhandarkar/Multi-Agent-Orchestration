import os
import sys
import pickle
import faiss
from src.core.config import settings
from src.utils.logger import get_logger
from src.utils.exception import CustomException

logger = get_logger(__name__)


class VectorStore:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self._model = None  # Lazy-loaded on first use to avoid 400MB RAM spike at startup
        self.index = None
        self.chunks: list[str] = []
        self.index_dir = settings.FAISS_INDEX_DIR

    @property
    def model(self):
        """Lazy-load SentenceTransformer only when first needed (saves ~400MB at startup)."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Lazy-loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _chunk_text(self, text: str, chunk_size: int = 100, overlap: float = 0.20) -> list[str]:
        words = text.split()
        step = int(chunk_size * (1 - overlap))
        chunks = []
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
        return chunks

    def build_index(self, source_path: str) -> None:
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                text = f.read()

            self.chunks = self._chunk_text(text)
            logger.info(f"Generated {len(self.chunks)} chunks from {source_path}")

            embeddings = self.model.encode(self.chunks, convert_to_numpy=True)
            faiss.normalize_L2(embeddings)

            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)
            self.index.add(embeddings)

            os.makedirs(self.index_dir, exist_ok=True)
            faiss.write_index(self.index, os.path.join(self.index_dir, "index.faiss"))
            with open(os.path.join(self.index_dir, "chunks.pkl"), "wb") as f:
                pickle.dump(self.chunks, f)

            logger.info(f"FAISS index persisted to {self.index_dir}")
        except Exception as e:
            raise CustomException(e, sys) from e

    def load_index(self) -> None:
        try:
            index_path = os.path.join(self.index_dir, "index.faiss")
            chunks_path = os.path.join(self.index_dir, "chunks.pkl")

            if not os.path.exists(index_path):
                raise FileNotFoundError(
                    f"No FAISS index found at {index_path}. Run build_index() first."
                )

            self.index = faiss.read_index(index_path)
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)

            logger.info(f"Loaded FAISS index with {len(self.chunks)} chunks")
        except Exception as e:
            raise CustomException(e, sys) from e

    def search(self, query: str, top_k: int = 2) -> list[dict]:
        try:
            if self.index is None:
                self.load_index()

            query_vec = self.model.encode([query], convert_to_numpy=True)
            faiss.normalize_L2(query_vec)

            scores, indices = self.index.search(query_vec, top_k)

            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:
                    continue
                results.append({"text": self.chunks[idx], "score": float(score)})

            return results
        except Exception as e:
            raise CustomException(e, sys) from e


if __name__ == "__main__":
    vs = VectorStore()
    vs.build_index("data/academic_regulations.txt")
