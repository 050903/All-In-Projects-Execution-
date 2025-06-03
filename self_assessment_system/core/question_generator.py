import json
import os
from typing import List, Dict, Any

QUESTIONS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'questions.json')

class QuestionGenerator:
    def __init__(self, questions_file: str = QUESTIONS_FILE_PATH):
        self.questions = self._load_questions(questions_file)

    def _load_questions(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
            if not isinstance(questions_data, list):
                raise ValueError("Questions data should be a list.")
            return questions_data
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file câu hỏi tại '{file_path}'")
            return []
        except json.JSONDecodeError:
            print(f"Lỗi: File câu hỏi '{file_path}' không phải là JSON hợp lệ.")
            return []
        except ValueError as e:
            print(f"Lỗi: {e}")
            return []

    def get_all_questions(self) -> List[Dict[str, Any]]:
        return self.questions

    def get_questions_by_category(self, category_name: str) -> List[Dict[str, Any]]:
        return [q for q in self.questions if q.get('category') == category_name]

    def get_question_by_id(self, question_id: str) -> Dict[str, Any] | None:
        for q in self.questions:
            if q.get('id') == question_id:
                return q
        return None

if __name__ == '__main__':
    # Test
    generator = QuestionGenerator()
    all_q = generator.get_all_questions()
    print(f"Tổng số câu hỏi: {len(all_q)}")
    if all_q:
        print("\nCâu hỏi đầu tiên:")
        print(json.dumps(all_q[0], indent=2, ensure_ascii=False))

    core_values_q = generator.get_questions_by_category("Giá trị cốt lõi")
    print(f"\nSố câu hỏi về Giá trị cốt lõi: {len(core_values_q)}")

    q_cv01 = generator.get_question_by_id("CV01")
    if q_cv01:
        print("\nThông tin câu hỏi CV01:")
        print(json.dumps(q_cv01, indent=2, ensure_ascii=False))