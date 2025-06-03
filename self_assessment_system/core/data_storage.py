import json
import os
import datetime
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class DataStorage:
    def __init__(self, data_directory: str = DATA_DIR):
        self.data_directory = data_directory
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

    def save_responses(self, user_id: str, responses: List[Dict[str, Any]], assessment_name: str = "general") -> bool:
        """
        Lưu trữ phản hồi của người dùng.
        responses: list of {"question_id": "...", "answer": "..."}
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"responses_{user_id}_{assessment_name}_{timestamp}.json"
        file_path = os.path.join(self.data_directory, filename)

        data_to_save = {
            "user_id": user_id,
            "assessment_name": assessment_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "responses": responses
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
            print(f"Đã lưu phản hồi vào: {file_path}")
            return True
        except IOError as e:
            print(f"Lỗi khi lưu file: {e}")
            return False

    def load_latest_response(self, user_id: str, assessment_name: str = "general") -> Dict[str, Any] | None:
        """Tải phản hồi gần nhất của người dùng cho một bài đánh giá cụ thể."""
        try:
            response_files = [
                f for f in os.listdir(self.data_directory)
                if f.startswith(f"responses_{user_id}_{assessment_name}_") and f.endswith(".json")
            ]
            if not response_files:
                return None

            latest_file = sorted(response_files, reverse=True)[0]
            file_path = os.path.join(self.data_directory, latest_file)

            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except IOError as e:
            print(f"Lỗi khi tải file: {e}")
            return None
        except json.JSONDecodeError:
            print(f"Lỗi: File phản hồi không phải là JSON hợp lệ.")
            return None


if __name__ == '__main__':
    # Test
    storage = DataStorage()
    user_responses_test = [
        {"question_id": "CV01", "answer": 4},
        {"question_id": "GI_L02", "answer": "Có"}
    ]
    storage.save_responses("test_user", user_responses_test)

    loaded_data = storage.load_latest_response("test_user")
    if loaded_data:
        print("\nDữ liệu phản hồi đã tải:")
        print(json.dumps(loaded_data, indent=2, ensure_ascii=False))