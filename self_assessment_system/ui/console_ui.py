import json
from typing import List, Dict, Any, Union

class ConsoleUI:
    def get_user_id(self) -> str:
        while True:
            user_id = input("Vui lòng nhập ID người dùng của bạn (ví dụ: ten_cua_ban): ").strip()
            if user_id:
                return user_id
            print("ID người dùng không được để trống.")

    def display_question(self, question: Dict[str, Any]) -> Any:
        print("\n" + "="*30)
        print(f"Câu hỏi (ID: {question['id']}, Danh mục: {question['category']}):")
        print(question['text'])

        q_type = question['type']
        answer = None

        if q_type == "likert":
            scale_min = question.get('scale_min', 1)
            scale_max = question.get('scale_max', 5)
            while True:
                try:
                    ans_str = input(f"Nhập câu trả lời của bạn ({scale_min}-{scale_max}): ")
                    ans_int = int(ans_str)
                    if scale_min <= ans_int <= scale_max:
                        answer = ans_int
                        break
                    else:
                        print(f"Vui lòng nhập một số từ {scale_min} đến {scale_max}.")
                except ValueError:
                    print("Vui lòng nhập một số hợp lệ.")
        elif q_type == "multiple_choice_single":
            options = question.get('options', [])
            for opt in options:
                print(f"  {opt['value']}. {opt['text']}")
            valid_options = [opt['value'] for opt in options]
            while True:
                ans_str = input(f"Chọn một đáp án ({', '.join(valid_options)}): ").strip().lower()
                if ans_str in valid_options:
                    answer = ans_str
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        elif q_type == "yes_no":
            while True:
                ans_str = input("Trả lời (Có/Không): ").strip().lower()
                if ans_str in ["có", "co", "c"]:
                    answer = "Có"
                    break
                elif ans_str in ["không", "khong", "k", "ko"]:
                    answer = "Không"
                    break
                else:
                    print("Vui lòng trả lời 'Có' hoặc 'Không'.")
        elif q_type == "open_short" or q_type == "open_long":
            answer = input("Nhập câu trả lời của bạn: ").strip()
        else:
            print(f"Loại câu hỏi '{q_type}' chưa được hỗ trợ trong UI này.")
            answer = input("Nhập câu trả lời của bạn: ").strip() # Fallback

        return answer

    def run_assessment(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        print("Chào mừng bạn đến với Hệ thống Tự Đánh Giá Cá Nhân!")
        user_responses: List[Dict[str, Any]] = []

        for i, q_data in enumerate(questions):
            print(f"\n--- Câu {i+1}/{len(questions)} ---")
            user_answer = self.display_question(q_data)
            user_responses.append({
                "question_id": q_data['id'],
                "answer": user_answer
            })
        print("\n" + "="*30)
        print("Cảm ơn bạn đã hoàn thành bài đánh giá!")
        return user_responses

if __name__ == '__main__':
    # Test
    # Tạo một vài câu hỏi mẫu để test UI
    sample_questions_for_ui_test = [
        {
            "id": "CV01_test",
            "category": "Giá trị cốt lõi",
            "text": "Mức độ quan trọng của 'Sự trung thực' (1-5)?",
            "type": "likert",
            "scale_min": 1,
            "scale_max": 5
        },
        {
            "id": "DM01_test",
            "category": "Động lực",
            "text": "Bạn thích làm việc độc lập hay nhóm?",
            "type": "multiple_choice_single",
            "options": [
                {"value": "a", "text": "Độc lập"},
                {"value": "b", "text": "Nhóm"}
            ]
        },
        {
            "id": "GI_L02_test",
            "category": "Trí thông minh Gardner",
            "text": "Bạn có thích đọc sách không?",
            "type": "yes_no"
        },
         {
            "id": "CV08_test",
            "category": "Giá trị cốt lõi",
            "text": "Giá trị quan trọng nhất của bạn là gì?",
            "type": "open_short"
        }
    ]
    ui = ConsoleUI()
    user_id_test = ui.get_user_id()
    print(f"User ID: {user_id_test}")
    responses = ui.run_assessment(sample_questions_for_ui_test)
    print("\nPhản hồi thu thập được:")
    print(json.dumps(responses, indent=2, ensure_ascii=False))