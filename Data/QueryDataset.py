import pandas as pd
from torch.utils.data import Dataset
import os
from Core.Common.Logger import logger

class RAGQueryDataset(Dataset):
    def __init__(self,data_dir):
        super().__init__()
      
        self.corpus_path = os.path.join(data_dir, "Corpus.json")
        self.qa_path = os.path.join(data_dir, "Question.json")
        
        try:
            self.dataset = pd.read_json(self.qa_path, lines=True, orient="records")
        except FileNotFoundError:
            raise FileNotFoundError(f"Question file not found: {self.qa_path}")
        except ValueError as e:
            raise ValueError(f"Error parsing question file {self.qa_path}: {e}")
            
        try:
            self.corpus = pd.read_json(self.corpus_path, lines=True)
        except FileNotFoundError:
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")
        except ValueError as e:
            raise ValueError(f"Error parsing corpus file {self.corpus_path}: {e}")

    def get_corpus(self):
        corpus_list = []
        for i in range(len(self.corpus)):
            corpus_list.append(
                {
                    "title": self.corpus.iloc[i]["title"],
                    "content": self.corpus.iloc[i]["context"],
                    "doc_id": i,
                }
            )
        return corpus_list

    def get_corpus_item(self, doc_id):
        """Get a single corpus item by doc_id
        
        Args:
            doc_id: Index of the corpus document (0-indexed)
            
        Returns:
            Dictionary with corpus item data
            
        Raises:
            IndexError: If doc_id is out of range
        """
        if doc_id < 0 or doc_id >= len(self.corpus):
            raise IndexError(f"doc_id {doc_id} is out of range. Corpus has {len(self.corpus)} documents.")
        
        return {
            "title": self.corpus.iloc[doc_id]["title"],
            "content": self.corpus.iloc[doc_id]["context"],
            "doc_id": doc_id,
        }
    
    def get_questions_for_corpus(self, doc_id):
        """Get all questions related to a specific corpus document"""
        # Try to find questions with matching doc_id or corpus_id field
        questions = []
        for idx in range(len(self.dataset)):
            question_data = self.__getitem__(idx)
            # Check if question belongs to this corpus (support both doc_id and corpus_id field names)
            q_doc_id = question_data.get('doc_id', question_data.get('corpus_id', None))
            if q_doc_id == doc_id:
                questions.append(question_data)
        return questions

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        question = self.dataset.iloc[idx]["question"]
        answer = self.dataset.iloc[idx]["answer"]
        # other_attrs = self.dataset.iloc[idx].drop(["answer", "question"])
        other_attrs = self.dataset.iloc[idx].drop(["answer", "question"])
        return {"id": idx, "question": question, "answer": answer, **other_attrs}


if __name__ == "__main__":
    corpus_path = "tmp.json"
    qa_path = "tmp.json"
    query_dataset = RAGQueryDataset(qa_path=qa_path, corpus_path=corpus_path)
    corpus = query_dataset.get_corpus()
    print(corpus[0])
    print(query_dataset[0])
