# self_assessment_system/core/analyzer.py
import pandas as pd
from typing import List, Dict, Any, Tuple

class Analyzer:
    def __init__(self, questions_data: List[Dict[str, Any]]):
        """
        Khởi tạo Analyzer với dữ liệu câu hỏi (bao gồm scoring_info).
        questions_data: List các dictionary câu hỏi từ QuestionGenerator.
        """
        self.questions_map = {q['id']: q for q in questions_data}

    def _get_score_for_response(self, question_id: str, answer: Any) -> Dict[str, float]:
        """
        Tính điểm cho một câu trả lời dựa trên scoring_info.
        Trả về một dict: {"dimension_name": score_value}
        """
        question_info = self.questions_map.get(question_id)
        if not question_info or 'scoring_info' not in question_info:
            return {} # Không có thông tin tính điểm

        scoring_info = question_info['scoring_info']
        q_type = question_info['type']
        scores = {}

        if q_type == "likert":
            dimension = scoring_info.get("dimension")
            interpretation = scoring_info.get("interpretation", "direct")
            if dimension and isinstance(answer, (int, float)):
                score = float(answer)
                if interpretation == "inverse":
                    # Đảo ngược điểm nếu cần (ví dụ: câu hỏi về mức độ căng thẳng)
                    # Giả sử thang điểm là scale_min đến scale_max
                    scale_min = question_info.get('scale_min', 1)
                    scale_max = question_info.get('scale_max', 5)
                    score = (scale_max + scale_min) - score
                scores[dimension] = score

        elif q_type == "yes_no":
            dimension = scoring_info.get("dimension")
            if dimension:
                if str(answer).lower() in ["có", "co", "c", "yes", "true", "1"]:
                    scores[dimension] = float(scoring_info.get("yes_value", 0))
                elif str(answer).lower() in ["không", "khong", "k", "ko", "no", "false", "0"]:
                    scores[dimension] = float(scoring_info.get("no_value", 0))

        elif q_type == "multiple_choice_single":
            # scoring_info cho multiple_choice_single có thể là:
            # {"a": {"dimension": "X", "points": 1}, "b": {"dimension": "Y", "points": 1}}
            # Hoặc đơn giản hơn: {"dimension": "CategoryX", "points_mapping": {"a": 1, "b": 0.5}}
            if str(answer) in scoring_info:
                choice_scoring = scoring_info[str(answer)]
                if isinstance(choice_scoring, dict) and "dimension" in choice_scoring and "points" in choice_scoring:
                    scores[choice_scoring["dimension"]] = float(choice_scoring["points"])

        # Các loại câu hỏi khác có thể cần logic phức tạp hơn
        # Câu hỏi mở thường không được tính điểm tự động ở đây

        return scores

    def calculate_overall_scores(self, user_responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Tính tổng điểm hoặc điểm trung bình cho mỗi khía cạnh (dimension).
        user_responses: list of {"question_id": "...", "answer": "..."}
        """
        dimension_scores_sum: Dict[str, float] = {}
        dimension_counts: Dict[str, int] = {}

        for response in user_responses:
            q_id = response['question_id']
            answer = response['answer']
            individual_scores = self._get_score_for_response(q_id, answer)

            for dim, score_val in individual_scores.items():
                dimension_scores_sum[dim] = dimension_scores_sum.get(dim, 0.0) + score_val
                dimension_counts[dim] = dimension_counts.get(dim, 0) + 1

        # Tính điểm trung bình (hoặc có thể là tổng điểm tùy theo thiết kế)
        # Ở đây ví dụ tính trung bình, nếu muốn tổng thì bỏ chia
        averaged_scores: Dict[str, float] = {}
        for dim, total_score in dimension_scores_sum.items():
            count = dimension_counts.get(dim, 1) # Tránh chia cho 0
            if count > 0 :
                 # Làm tròn đến 2 chữ số thập phân
                averaged_scores[dim] = round(total_score / count, 2)
            else:
                averaged_scores[dim] = 0.0


        return averaged_scores

    def identify_strengths_weaknesses(self, overall_scores: Dict[str, float], top_n: int = 3) -> Dict[str, List[Tuple[str, float]]]:
        """
        Xác định điểm mạnh và điểm yếu dựa trên điểm số tổng thể.
        Trả về dict {"strengths": [...], "weaknesses": [...]}
        """
        if not overall_scores:
            return {"strengths": [], "weaknesses": []}

        sorted_scores = sorted(overall_scores.items(), key=lambda item: item[1], reverse=True)

        strengths = sorted_scores[:top_n]
        # Điểm yếu có thể là những điểm thấp nhất, hoặc những điểm dưới một ngưỡng nào đó
        # Ở đây lấy top_n thấp nhất
        weaknesses = sorted_scores[-top_n:]
        weaknesses.reverse() # Để hiển thị từ thấp nhất đến cao hơn một chút

        return {"strengths": strengths, "weaknesses": weaknesses}

    def analyze_value_proportions(self, user_responses: List[Dict[str, Any]], category_filter: str = "Giá trị cốt lõi") -> Dict[str, float]:
        """
        Phân tích tỷ lệ lựa chọn cho các câu hỏi trong một danh mục cụ thể (ví dụ: Giá trị cốt lõi).
        Hữu ích cho các câu hỏi lựa chọn ưu tiên.
        """
        value_counts: Dict[str, int] = {}
        total_relevant_questions = 0

        for response in user_responses:
            q_id = response['question_id']
            answer = str(response['answer']) # Đảm bảo answer là string để làm key
            question_info = self.questions_map.get(q_id)

            if question_info and question_info.get('category') == category_filter:
                # Logic này cần cụ thể hóa dựa trên cách bạn muốn phân tích giá trị
                # Ví dụ: nếu câu hỏi là lựa chọn ưu tiên, và answer là 'a', 'b', 'c'
                # bạn có thể muốn đếm số lần 'a' được chọn.
                # Hoặc nếu câu hỏi là Likert về một giá trị, bạn có thể tính điểm trung bình cho giá trị đó.

                # Ví dụ đơn giản: đếm số lần một lựa chọn cụ thể được chọn
                # (cần `scoring_info` hoặc cấu trúc `options` rõ ràng hơn để làm điều này tốt)
                # Giả sử câu hỏi multiple_choice_single và answer là value của option
                if question_info['type'] == "multiple_choice_single":
                    for opt in question_info.get('options', []):
                        if opt['value'] == answer:
                            value_counts[opt['text']] = value_counts.get(opt['text'], 0) + 1
                            break # Tìm thấy lựa chọn
                    total_relevant_questions +=1 # Hoặc logic đếm khác

        # Tính tỷ lệ phần trăm
        proportions: Dict[str, float] = {}
        # total_selections = sum(value_counts.values()) # Nếu đếm theo lựa chọn
        # Sử dụng total_relevant_questions nếu mỗi câu hỏi đóng góp 1 lần
        if total_relevant_questions > 0:
            for value_text, count in value_counts.items():
                proportions[value_text] = round((count / total_relevant_questions) * 100, 1)

        return proportions


    def analyze_motivation_trends(self, user_responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Phân tích xu hướng động lực (ví dụ: Nội tại vs. Ngoại tại).
        Cần `scoring_info` trong `questions.json` để ánh xạ câu trả lời với loại động lực.
        """
        motivation_scores: Dict[str, float] = {} # Ví dụ: {"Intrinsic Motivation": 3, "Extrinsic Motivation": 2}
        motivation_counts: Dict[str, int] = {}

        for response in user_responses:
            q_id = response['question_id']
            answer = response['answer']
            question_info = self.questions_map.get(q_id)

            if question_info and question_info.get('category') == "Động lực học tập và hành động" and 'scoring_info' in question_info:
                q_scoring_info = question_info['scoring_info']
                q_type = question_info['type']

                if q_type == "multiple_choice_single" and str(answer) in q_scoring_info:
                    choice_score_info = q_scoring_info[str(answer)]
                    if "dimension" in choice_score_info and "points" in choice_score_info:
                        dim = choice_score_info["dimension"]
                        points = float(choice_score_info["points"])
                        motivation_scores[dim] = motivation_scores.get(dim, 0.0) + points
                        motivation_counts[dim] = motivation_counts.get(dim, 0) + 1
                elif q_type == "likert" and "dimension" in q_scoring_info: # Nếu có câu hỏi likert về động lực
                    dim = q_scoring_info["dimension"]
                    points = float(answer) # Giả sử điểm trực tiếp
                    motivation_scores[dim] = motivation_scores.get(dim, 0.0) + points
                    motivation_counts[dim] = motivation_counts.get(dim, 0) + 1


        # Tính điểm trung bình cho mỗi loại động lực
        averaged_motivation_scores: Dict[str, float] = {}
        for dim, total_score in motivation_scores.items():
            count = motivation_counts.get(dim, 1)
            if count > 0:
                averaged_motivation_scores[dim] = round(total_score / count, 2)
        return averaged_motivation_scores


if __name__ == '__main__':
    # --- Test Analyzer ---
    # Giả sử bạn đã có QuestionGenerator và tải được questions.json
    from core.question_generator import QuestionGenerator # Đặt ở đầu file nếu chưa có
    q_gen = QuestionGenerator()
    all_questions_data = q_gen.get_all_questions()

    if not all_questions_data:
        print("Không thể tải câu hỏi để test Analyzer.")
    else:
        analyzer = Analyzer(all_questions_data)

        # Tạo dữ liệu phản hồi mẫu
        sample_user_responses = [
            {"question_id": "CV01", "answer": 5}, # Honesty & Integrity
            {"question_id": "GI_L01", "answer": 4}, # Linguistic
            {"question_id": "GI_L02", "answer": "Có"}, # Linguistic (yes_value = 1)
            {"question_id": "DM01", "answer": "a"}, # Intrinsic Motivation
            # Thêm các câu trả lời khác để có nhiều khía cạnh
            {"question_id": "CV06", "answer": "c"}, # Giá trị cốt lõi - lựa chọn
            # ...
        ]
        # Cần đảm bảo các ID câu hỏi này có trong questions.json và có scoring_info

        print("--- Tính điểm tổng thể ---")
        overall_scores = analyzer.calculate_overall_scores(sample_user_responses)
        print(overall_scores) # Output: {'Honesty & Integrity': 5.0, 'Linguistic Intelligence': 2.5, 'Intrinsic Motivation': 1.0} (ví dụ)

        print("\n--- Điểm mạnh/yếu ---")
        strengths_weaknesses = analyzer.identify_strengths_weaknesses(overall_scores)
        print(strengths_weaknesses)

        print("\n--- Phân tích tỷ lệ giá trị (ví dụ) ---")
        # Cần câu hỏi Giá trị cốt lõi dạng multiple_choice_single với scoring phù hợp
        value_proportions = analyzer.analyze_value_proportions(sample_user_responses)
        print(value_proportions)

        print("\n--- Phân tích xu hướng động lực ---")
        motivation_trends = analyzer.analyze_motivation_trends(sample_user_responses)
        print(motivation_trends)