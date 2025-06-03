# self_assessment_system/streamlit_app.py
import streamlit as st
from core.question_generator import QuestionGenerator
from core.data_storage import DataStorage
from core.analyzer import Analyzer
from visualization.plotter import Plotter # Plotly sẽ hiển thị trực tiếp trong Streamlit
from reporting.report_generator import ReportGenerator # Có thể hiển thị HTML hoặc link tải
import os
import json # Để hiển thị debug

# --- Khởi tạo các đối tượng dùng chung ---
# Nên cache để tránh tải lại câu hỏi mỗi lần tương tác
@st.cache_resource # Dùng cache_resource cho các đối tượng không thể hash
def load_question_generator():
    return QuestionGenerator()

@st.cache_resource
def get_data_storage():
    return DataStorage()

@st.cache_resource
def get_plotter():
    return Plotter(output_dir="output_charts_streamlit") # Thư mục riêng cho streamlit

@st.cache_resource
def get_report_generator():
    return ReportGenerator(output_dir="output_reports_streamlit")


q_generator = load_question_generator()
storage = get_data_storage()
plotter = get_plotter() # Plotter sẽ được dùng để tạo ảnh cho report, hoặc vẽ trực tiếp
reporter = get_report_generator()
all_questions_data = q_generator.get_all_questions()
# Analyzer cần all_questions_data, khởi tạo khi cần
# analyzer = Analyzer(all_questions_data)


def display_streamlit_question(question_data, question_key_suffix):
    st.subheader(f"Câu hỏi (ID: {question_data['id']})")
    st.write(f"**Danh mục:** {question_data['category']}")
    st.markdown(question_data['text']) # Dùng markdown để hiển thị text tốt hơn

    q_type = question_data['type']
    q_id = question_data['id']
    # Tạo key duy nhất cho mỗi widget Streamlit để tránh lỗi DuplicateWidgetID
    widget_key = f"{q_id}_{question_key_suffix}"

    answer = None
    if q_type == "likert":
        scale_min = question_data.get('scale_min', 1)
        scale_max = question_data.get('scale_max', 5)
        answer = st.slider("Câu trả lời của bạn:", min_value=scale_min, max_value=scale_max, value=(scale_min + scale_max) // 2, key=widget_key)
    elif q_type == "multiple_choice_single":
        options_dict = {opt['text']: opt['value'] for opt in question_data.get('options', [])}
        # Hiển thị text cho người dùng, nhưng lưu value
        selected_text = st.radio("Chọn một đáp án:", options=list(options_dict.keys()), key=widget_key)
        if selected_text:
            answer = options_dict[selected_text]
    elif q_type == "yes_no":
        # selected_option = st.radio("Trả lời:", options=["Có", "Không"], index=None, key=widget_key)
        # answer = selected_option
        # Hoặc dùng selectbox để có placeholder
        selected_option = st.selectbox("Trả lời:", options=["", "Có", "Không"], format_func=lambda x: x if x else "Chọn...", key=widget_key)
        if selected_option:
            answer = selected_option

    elif q_type == "open_short":
        answer = st.text_input("Nhập câu trả lời ngắn:", key=widget_key)
    elif q_type == "open_long":
        answer = st.text_area("Nhập câu trả lời chi tiết:", key=widget_key)
    else:
        st.warning(f"Loại câu hỏi '{q_type}' chưa được hỗ trợ đầy đủ trong UI này.")
        answer = st.text_input("Nhập câu trả lời (fallback):", key=widget_key)
    return answer


def run_streamlit_assessment():
    st.title("📝 Hệ Thống Tự Đánh Giá Cá Nhân")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'user_responses' not in st.session_state:
        st.session_state.user_responses = []
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False
    if 'show_report' not in st.session_state:
        st.session_state.show_report = False


    if not st.session_state.assessment_complete:
        # --- Giai đoạn nhập User ID ---
        if not st.session_state.user_id:
            user_id_input = st.text_input("Vui lòng nhập Tên hoặc ID của bạn:", key="user_id_input")
            if st.button("Bắt đầu", key="start_button"):
                if user_id_input:
                    st.session_state.user_id = user_id_input
                    st.rerun() # Chạy lại script để cập nhật UI
                else:
                    st.error("Tên/ID không được để trống.")
            return # Dừng ở đây cho đến khi có user_id

        st.info(f"Chào mừng, {st.session_state.user_id}!")

        # --- Giai đoạn trả lời câu hỏi ---
        num_questions = len(all_questions_data)
        current_idx = st.session_state.current_question_index

        if current_idx < num_questions:
            question = all_questions_data[current_idx]
            st.progress((current_idx + 1) / num_questions)
            st.markdown(f"--- **Câu {current_idx + 1} / {num_questions}** ---")

            # Sử dụng form để nhóm câu hỏi và nút bấm
            with st.form(key=f"question_form_{current_idx}"):
                user_answer = display_streamlit_question(question, f"q{current_idx}")
                # Nút "Tiếp theo" và "Lùi lại" (nếu muốn)
                cols = st.columns(2)
                submitted_next = cols[1].form_submit_button("Tiếp theo ❯")
                # submitted_prev = cols[0].form_submit_button("❮ Lùi lại", disabled=(current_idx == 0))


                if submitted_next:
                    # Lưu câu trả lời hiện tại (nếu có)
                    # Cần đảm bảo user_answer không phải là None hoặc rỗng nếu câu hỏi yêu cầu
                    is_required = question['type'] not in ['open_short', 'open_long'] # Ví dụ đơn giản
                    if is_required and (user_answer is None or str(user_answer).strip() == ""):
                        st.warning("Vui lòng trả lời câu hỏi này.")
                    else:
                        # Ghi đè nếu câu hỏi đã được trả lời trước đó (khi dùng nút back)
                        found = False
                        for i, resp in enumerate(st.session_state.user_responses):
                            if resp['question_id'] == question['id']:
                                st.session_state.user_responses[i]['answer'] = user_answer
                                found = True
                                break
                        if not found:
                            st.session_state.user_responses.append({
                                "question_id": question['id'],
                                "answer": user_answer
                            })

                        st.session_state.current_question_index += 1
                        st.rerun()

                # if submitted_prev:
                #     st.session_state.current_question_index -= 1
                #     st.rerun()

        else: # Đã trả lời hết câu hỏi
            st.success("🎉 Bạn đã hoàn thành bài đánh giá!")
            st.session_state.assessment_complete = True
            # Lưu trữ kết quả
            if st.session_state.user_responses:
                storage.save_responses(st.session_state.user_id, st.session_state.user_responses, assessment_name="streamlit_assessment_v1")
                st.info("Kết quả của bạn đã được lưu lại.")
            if st.button("Xem Kết Quả Phân Tích", key="view_results_button"):
                st.session_state.show_report = True
                st.rerun()

    # --- Giai đoạn hiển thị báo cáo ---
    if st.session_state.assessment_complete and st.session_state.show_report:
        st.header("📊 Kết Quả Phân Tích Cá Nhân")

        # Tải lại phản hồi mới nhất để đảm bảo (hoặc dùng từ session_state nếu tin cậy)
        user_final_responses = st.session_state.user_responses
        # Hoặc:
        # latest_data = storage.load_latest_response(st.session_state.user_id, "streamlit_assessment_v1")
        # user_final_responses = latest_data['responses'] if latest_data else []


        if not user_final_responses:
            st.error("Không tìm thấy dữ liệu phản hồi để phân tích.")
            return

        analyzer = Analyzer(all_questions_data) # Khởi tạo analyzer ở đây
        overall_scores = analyzer.calculate_overall_scores(user_final_responses)
        strengths_weaknesses = analyzer.identify_strengths_weaknesses(overall_scores)
        value_proportions = analyzer.analyze_value_proportions(user_final_responses, category_filter="Giá trị cốt lõi")
        motivation_trends = analyzer.analyze_motivation_trends(user_final_responses)

        open_ended_responses_formatted = []
        for resp in user_final_responses:
            q_info = q_generator.get_question_by_id(resp['question_id'])
            if q_info and q_info['type'] in ['open_short', 'open_long'] and resp['answer']:
                open_ended_responses_formatted.append({
                    "question_text": q_info['text'],
                    "answer": resp['answer']
                })

        # --- Hiển thị biểu đồ trực tiếp với Plotly ---
        st.subheader("Bản đồ năng lực cá nhân")
        main_dimensions_for_radar = {
            k: v for k, v in overall_scores.items()
            if k in ["Linguistic Intelligence", "Logical-Mathematical Intelligence", "Spatial Intelligence",
                     "Bodily-Kinesthetic Intelligence", "Musical Intelligence", "Interpersonal Intelligence",
                     "Intrapersonal Intelligence", "Honesty & Integrity", "Intrinsic Motivation"] # Cập nhật danh sách này
        }
        main_dimensions_for_radar = {k: overall_scores.get(k, 0) for k in main_dimensions_for_radar.keys()}
        valid_radar_scores = {k: v for k, v in main_dimensions_for_radar.items() if isinstance(v, (int, float))}

        if valid_radar_scores:
            categories_radar = list(valid_radar_scores.keys())
            values_radar = list(valid_radar_scores.values())
            categories_radar_closed = categories_radar + [categories_radar[0]]
            values_radar_closed = values_radar + [values_radar[0]]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=values_radar_closed, theta=categories_radar_closed, fill='toself', name=f'Hồ sơ'))
            max_val_radar = max(values_radar) if values_radar else 5
            radial_range_radar = [0, max(5, np.ceil(max_val_radar))]
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=radial_range_radar)))
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.write("Không đủ dữ liệu để vẽ biểu đồ radar.")

        st.subheader("Điểm mạnh và lĩnh vực cần chú ý")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h5>Điểm mạnh:</h5>", unsafe_allow_html=True)
            if strengths_weaknesses["strengths"]:
                for item, score in strengths_weaknesses["strengths"]:
                    st.markdown(f"- {item}: **{score}**")
            else:
                st.write("Chưa xác định.")
        with col2:
            st.markdown("<h5>Lĩnh vực cần chú ý:</h5>", unsafe_allow_html=True)
            if strengths_weaknesses["weaknesses"]:
                for item, score in strengths_weaknesses["weaknesses"]:
                    st.markdown(f"- {item}: **{score}**")
            else:
                st.write("Chưa xác định.")


        if value_proportions:
            st.subheader("Tỷ lệ Giá trị cốt lõi")
            fig_pie_values = go.Figure(data=[go.Pie(labels=list(value_proportions.keys()),
                                                   values=list(value_proportions.values()), hole=.3)])
            st.plotly_chart(fig_pie_values, use_container_width=True)

        if motivation_trends:
            st.subheader("Xu hướng Động lực")
            # Có thể dùng Bar chart thay vì Pie nếu có nhiều loại động lực
            fig_pie_motivation = go.Figure(data=[go.Pie(labels=list(motivation_trends.keys()),
                                                       values=list(motivation_trends.values()), hole=.3)])
            st.plotly_chart(fig_pie_motivation, use_container_width=True)

        if open_ended_responses_formatted:
            st.subheader("Phản hồi câu hỏi mở")
            for resp_data in open_ended_responses_formatted:
                with st.expander(f"Câu hỏi: {resp_data['question_text'][:50]}..."): # Rút gọn text câu hỏi
                    st.write(resp_data['answer'])

        # --- Nút tải báo cáo HTML (tùy chọn) ---
        # Tạo báo cáo HTML và cung cấp link tải
        # Cần đảm bảo plotter đã lưu ảnh nếu báo cáo HTML dùng ảnh từ file
        # Hoặc sửa ReportGenerator để nhận đối tượng Figure của Plotly và nhúng base64
        st.markdown("---")
        if st.button("Tạo và Tải Báo cáo HTML Chi tiết", key="download_html_report"):
            # Cần tạo lại các chart paths nếu ReportGenerator cần
            chart_paths_for_report = {} # Logic tạo chart paths tương tự main_console
            # Ví dụ:
            if valid_radar_scores:
                radar_files_report = plotter.create_radar_chart_plotly(valid_radar_scores, st.session_state.user_id, f"Bản đồ năng lực - {st.session_state.user_id}")
                chart_paths_for_report["radar_png"] = radar_files_report.get("png")

            # ... (tạo các chart khác cho báo cáo nếu cần)

            html_report_path = reporter.generate_html_report(
                st.session_state.user_id,
                overall_scores,
                strengths_weaknesses,
                value_proportions,
                motivation_trends,
                open_ended_responses_formatted,
                chart_paths_for_report # Truyền các đường dẫn ảnh đã lưu
            )
            if html_report_path and os.path.exists(html_report_path):
                with open(html_report_path, "rb") as fp:
                    st.download_button(
                        label="Tải xuống Báo cáo HTML",
                        data=fp,
                        file_name=os.path.basename(html_report_path),
                        mime="text/html"
                    )
            else:
                st.error("Không thể tạo file báo cáo HTML.")


        if st.button("Làm bài đánh giá mới", key="restart_assessment"):
            # Reset session state
            for key in list(st.session_state.keys()):
                if key not in ['user_id']: # Giữ lại user_id nếu muốn
                     del st.session_state[key]
            # Hoặc reset cụ thể:
            # st.session_state.current_question_index = 0
            # st.session_state.user_responses = []
            # st.session_state.assessment_complete = False
            # st.session_state.show_report = False
            st.rerun()

# Chạy ứng dụng Streamlit
if __name__ == "__main__":
    if not all_questions_data:
        st.error("Lỗi nghiêm trọng: Không thể tải file câu hỏi 'assets/questions.json'. Vui lòng kiểm tra file và đường dẫn.")
    else:
        run_streamlit_assessment()