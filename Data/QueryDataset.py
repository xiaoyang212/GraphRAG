import pandas as pd
from torch.utils.data import Dataset
import os

class RAGQueryDataset(Dataset):
    def __init__(self,data_dir):
        super().__init__()
      
        self.corpus_path = os.path.join(data_dir, "Corpus.json")
        self.qa_path = os.path.join(data_dir, "Question.json")
        self.dataset = pd.read_json(self.qa_path, lines=True, orient="records")
        self.corpus = pd.read_json(self.corpus_path, lines=True)

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
        """Get a single corpus item by doc_id"""
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
