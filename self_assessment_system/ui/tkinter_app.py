# self_assessment_system/ui/tkinter_app.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkFont
from PIL import Image, ImageTk
import os
import sys
import webbrowser
import numpy as np # Import numpy vì plotter có thể dùng

# Thêm đường dẫn gốc của dự án vào sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.question_generator import QuestionGenerator
from core.data_storage import DataStorage
from core.analyzer import Analyzer
from visualization.plotter import Plotter
from reporting.report_generator import ReportGenerator

# --- Định nghĩa màu sắc và font chữ ---
BG_COLOR = "#ECECEC"
FRAME_BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#333333"
ACCENT_COLOR = "#007ACC"
BUTTON_TEXT_COLOR = "#FFFFFF"
ERROR_COLOR = "#D32F2F"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEADING = ("Segoe UI", 16, "bold")
FONT_SUBHEADING = ("Segoe UI", 12, "italic")
FONT_NORMAL = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 11, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_QUESTION_CATEGORY = ("Segoe UI", 10, "bold")
FONT_QUESTION_TEXT = ("Segoe UI", 12)

class EnhancedTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InsightMe - Hệ Thống Tự Đánh Giá Cá Nhân")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=BG_COLOR)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("Content.TFrame", background=FRAME_BG_COLOR, relief="solid", borderwidth=1, padding=10)
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_NORMAL)
        self.style.configure("Title.TLabel", font=FONT_TITLE, foreground=ACCENT_COLOR, background=FRAME_BG_COLOR)
        self.style.configure("Heading.TLabel", font=FONT_HEADING, background=BG_COLOR, foreground=ACCENT_COLOR)
        self.style.configure("FrameHeading.TLabel", font=FONT_HEADING, background=FRAME_BG_COLOR, foreground=ACCENT_COLOR)
        self.style.configure("Subheading.TLabel", font=FONT_SUBHEADING, background=BG_COLOR)
        self.style.configure("FrameSubheading.TLabel", font=FONT_SUBHEADING, background=FRAME_BG_COLOR)
        self.style.configure("Error.TLabel", foreground=ERROR_COLOR, background=FRAME_BG_COLOR, font=FONT_SMALL)
        self.style.configure("TButton", font=FONT_BUTTON, background=ACCENT_COLOR, foreground=BUTTON_TEXT_COLOR, padding=(15, 8), borderwidth=0)
        self.style.map("TButton", background=[('active', '#005A9E'), ('pressed', '#004C8A')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        self.style.configure("TRadiobutton", background=FRAME_BG_COLOR, font=FONT_NORMAL, indicatorrelief='flat', padding=(5,2))
        self.style.map("TRadiobutton", background=[('active', '#E0E0E0')])
        self.style.configure("TEntry", fieldbackground=FRAME_BG_COLOR, font=FONT_NORMAL, padding=7)
        self.style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        self.style.configure("TNotebook.Tab", font=FONT_BUTTON, padding=(12, 7), background=BG_COLOR, borderwidth=1)
        self.style.map("TNotebook.Tab",
                       background=[("selected", FRAME_BG_COLOR), ('!selected', BG_COLOR), ('active', '#D8E6F3')],
                       foreground=[("selected", ACCENT_COLOR), ('!selected', TEXT_COLOR), ('active', ACCENT_COLOR)],
                       bordercolor=[("selected", ACCENT_COLOR)],
                       lightcolor=[("selected", FRAME_BG_COLOR)],
                       focuscolor=self.style.lookup("TNotebook.Tab", "focuscolor"))

        self.q_generator = QuestionGenerator()
        self.all_questions = self.q_generator.get_all_questions()
        if not self.all_questions:
            messagebox.showerror("Lỗi nghiêm trọng", "Không thể tải file câu hỏi 'assets/questions.json'.\nVui lòng kiểm tra lại file và khởi động lại ứng dụng.")
            self.root.destroy()
            return

        self.storage = DataStorage()
        self.analyzer = Analyzer(self.all_questions)
        self.plotter = Plotter(output_dir="output_charts_tkinter_enhanced")
        self.reporter = ReportGenerator(output_dir="output_reports_tkinter_enhanced")

        self.current_question_index = 0
        self.user_responses = []
        self.user_id = ""
        self.text_answer_widget = None # Khởi tạo ở đây

        self.container_frame = ttk.Frame(self.root, style="TFrame")
        self.container_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.setup_user_id_input()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def create_styled_frame(self, parent, style="Content.TFrame"):
        frame = ttk.Frame(parent, style=style)
        return frame

    def setup_user_id_input(self):
        self.clear_frame(self.container_frame)
        content_frame = self.create_styled_frame(self.container_frame)
        content_frame.pack(pady=100, padx=100, fill="x", expand=False)

        ttk.Label(content_frame, text="Chào Mừng Đến Với InsightMe!", style="Title.TLabel").pack(pady=(10, 25))
        ttk.Label(content_frame, text="Vui lòng nhập Tên hoặc ID của bạn:", style="FrameSubheading.TLabel").pack(pady=10)

        self.user_id_entry_var = tk.StringVar()
        self.user_id_entry = ttk.Entry(content_frame, width=40, textvariable=self.user_id_entry_var, font=FONT_NORMAL)
        self.user_id_entry.pack(pady=5, ipady=3)
        self.user_id_entry.focus()

        self.error_label_userid = ttk.Label(content_frame, text="", style="Error.TLabel")
        self.error_label_userid.pack(pady=(0,10))

        ttk.Button(content_frame, text="Bắt đầu Đánh Giá", command=self.start_assessment, style="TButton").pack(pady=20, ipadx=10)
        self.root.bind('<Return>', self.start_assessment)

    def start_assessment(self, event=None):
        self.user_id = self.user_id_entry_var.get().strip()
        if not self.user_id:
            self.error_label_userid.config(text="Tên/ID không được để trống.")
            return
        self.error_label_userid.config(text="")
        self.root.unbind('<Return>')
        self.current_question_index = 0
        self.user_responses = []
        self.display_current_question()

    def display_current_question(self):
        self.clear_frame(self.container_frame)
        content_frame = self.create_styled_frame(self.container_frame)
        content_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        if not (0 <= self.current_question_index < len(self.all_questions)):
            self.finish_assessment()
            return

        question_data = self.all_questions[self.current_question_index]

        header_frame = ttk.Frame(content_frame, style="Content.TFrame", padding=(10,5))
        header_frame.pack(fill=tk.X, pady=(0, 15))
        progress_text = f"Câu hỏi {self.current_question_index + 1} / {len(self.all_questions)}"
        ttk.Label(header_frame, text=progress_text, font=FONT_SMALL, style="FrameSubheading.TLabel").pack(side=tk.LEFT)
        ttk.Label(header_frame, text=f"Danh mục: {question_data['category']}", font=FONT_QUESTION_CATEGORY, style="FrameSubheading.TLabel").pack(side=tk.RIGHT)

        question_text_frame = ttk.Frame(content_frame, style="Content.TFrame", padding=15)
        question_text_frame.pack(fill=tk.X, pady=10)
        question_text_label = ttk.Label(question_text_frame, text=question_data['text'],
                                       wraplength=750, justify=tk.LEFT, font=FONT_QUESTION_TEXT, style="FrameSubheading.TLabel")
        question_text_label.pack(anchor="w")

        self.current_answer_var = None
        self.text_answer_widget = None # Reset trước khi tạo mới
        options_outer_frame = ttk.Frame(content_frame, style="Content.TFrame", padding=15)
        options_outer_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        q_type = question_data['type']

        if q_type == "likert":
            self.current_answer_var = tk.IntVar(value=0)
            scale_min = question_data.get('scale_min', 1)
            scale_max = question_data.get('scale_max', 5)
            desc_frame = ttk.Frame(options_outer_frame, style="Content.TFrame")
            desc_frame.pack(fill=tk.X, pady=(0,10))
            ttk.Label(desc_frame, text=f"{scale_min} (Rất không đồng ý/Không đúng)", font=FONT_SMALL, style="FrameSubheading.TLabel").pack(side=tk.LEFT)
            ttk.Label(desc_frame, text=f"{scale_max} (Rất đồng ý/Rất đúng)", font=FONT_SMALL, style="FrameSubheading.TLabel").pack(side=tk.RIGHT)
            buttons_frame = ttk.Frame(options_outer_frame, style="Content.TFrame")
            buttons_frame.pack(pady=5)
            for i in range(scale_min, scale_max + 1):
                rb = ttk.Radiobutton(buttons_frame, text=str(i), variable=self.current_answer_var, value=i, style="TRadiobutton")
                rb.pack(side=tk.LEFT, padx=20, ipady=5)
        elif q_type in ["multiple_choice_single", "yes_no"]:
            self.current_answer_var = tk.StringVar(value="")
            options_to_display = question_data.get('options', []) if q_type == "multiple_choice_single" else \
                                 [{"value": "Có", "text": "Có"}, {"value": "Không", "text": "Không"}]
            for opt in options_to_display:
                rb = ttk.Radiobutton(options_outer_frame, text=opt['text'],
                                     variable=self.current_answer_var, value=opt['value'], style="TRadiobutton")
                rb.pack(anchor="w", pady=4, padx=5)
        elif q_type in ["open_short", "open_long"]:
            # self.current_answer_var sẽ được dùng cho open_short
            # self.text_answer_widget sẽ được dùng cho open_long
            if q_type == "open_long":
                text_frame = ttk.Frame(options_outer_frame, style="Content.TFrame")
                text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
                self.text_answer_widget = tk.Text(text_frame, height=7, width=70, font=FONT_NORMAL, relief=tk.SOLID,
                                                 borderwidth=1, padx=7, pady=7, wrap=tk.WORD,
                                                 background=FRAME_BG_COLOR, foreground=TEXT_COLOR)
                scrollbar_text = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_answer_widget.yview)
                self.text_answer_widget.configure(yscrollcommand=scrollbar_text.set)
                scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
                self.text_answer_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                # Không set self.current_answer_var cho open_long nữa
            else: # open_short
                self.current_answer_var = tk.StringVar()
                entry = ttk.Entry(options_outer_frame, textvariable=self.current_answer_var, width=80, font=FONT_NORMAL)
                entry.pack(anchor="w", pady=5, ipady=3)
        else:
            ttk.Label(options_outer_frame, text=f"Loại câu hỏi '{q_type}' chưa được hỗ trợ.", style="FrameSubheading.TLabel").pack(anchor="w")

        nav_frame = ttk.Frame(content_frame, style="Content.TFrame", padding=(10,15))
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10,0))
        if self.current_question_index > 0:
             ttk.Button(nav_frame, text="❮  Lùi lại", command=self.prev_question, style="TButton").pack(side=tk.LEFT, padx=20)
        self.next_button_text = "Tiếp theo ❯" if self.current_question_index < len(self.all_questions) - 1 else "Hoàn thành ✔"
        self.next_button = ttk.Button(nav_frame, text=self.next_button_text, command=self.next_or_finish, style="TButton")
        self.next_button.pack(side=tk.RIGHT, padx=20)

        self.load_previous_answer()

    def record_current_answer(self):
        if not (0 <= self.current_question_index < len(self.all_questions)): return False
        q_data = self.all_questions[self.current_question_index]
        answer_value = None

        if q_data['type'] == "open_long" and self.text_answer_widget:
            answer_value = self.text_answer_widget.get("1.0", tk.END).strip()
        elif self.current_answer_var: # Gồm cả open_short, likert, mcq, yes_no
            answer_value = self.current_answer_var.get()


        existing_response_index = -1
        for i, resp in enumerate(self.user_responses):
            if resp['question_id'] == q_data['id']:
                existing_response_index = i
                break

        is_valid_answer = False
        if isinstance(answer_value, str) and answer_value.strip():
            is_valid_answer = True
        elif isinstance(answer_value, int) and answer_value != 0: # Likert không chọn là 0
             is_valid_answer = True


        if is_valid_answer:
            response_entry = {"question_id": q_data['id'], "answer": answer_value}
            if existing_response_index != -1:
                self.user_responses[existing_response_index] = response_entry
            else:
                self.user_responses.append(response_entry)
            return True
        elif existing_response_index != -1: # Nếu câu trả lời cũ có, giờ thành không hợp lệ -> xóa
            del self.user_responses[existing_response_index]
        return False


    def next_or_finish(self):
        if not (0 <= self.current_question_index < len(self.all_questions)): return

        q_data = self.all_questions[self.current_question_index]
        q_type = q_data['type']
        is_answered_or_optional = (q_type in ["open_short", "open_long"]) # Câu mở có thể bỏ qua

        if not is_answered_or_optional:
            current_val = None
            if self.current_answer_var: # For likert, mcq, yes_no
                current_val = self.current_answer_var.get()

            is_valid_for_non_open = False
            if isinstance(current_val, str) and current_val.strip(): # mcq, yes_no
                is_valid_for_non_open = True
            elif isinstance(current_val, int) and current_val != 0: # likert
                is_valid_for_non_open = True

            if not is_valid_for_non_open:
                messagebox.showwarning("Chưa trả lời", "Vui lòng cung cấp câu trả lời cho câu hỏi này.")
                return

        self.record_current_answer()

        if self.current_question_index < len(self.all_questions) - 1:
            self.current_question_index += 1
            self.display_current_question()
        else:
            self.finish_assessment()

    def prev_question(self):
        if self.current_question_index > 0:
            self.record_current_answer()
            self.current_question_index -= 1
            self.display_current_question()

    def load_previous_answer(self):
        if not (0 <= self.current_question_index < len(self.all_questions)): return

        q_data = self.all_questions[self.current_question_index]
        q_type = q_data['type']
        found_previous_answer = False

        for resp in self.user_responses:
            if resp['question_id'] == q_data['id']:
                if q_type == "open_long" and self.text_answer_widget:
                    self.text_answer_widget.delete("1.0", tk.END)
                    self.text_answer_widget.insert("1.0", resp['answer'])
                    found_previous_answer = True
                elif self.current_answer_var: # Gồm cả open_short
                    self.current_answer_var.set(resp['answer'])
                    found_previous_answer = True
                break # Đã tìm thấy

        if not found_previous_answer:
            if q_type == "open_long" and self.text_answer_widget:
                self.text_answer_widget.delete("1.0", tk.END)
            elif isinstance(self.current_answer_var, tk.IntVar): # Likert
                self.current_answer_var.set(0)
            elif isinstance(self.current_answer_var, tk.StringVar): # mcq, yes_no, open_short
                self.current_answer_var.set("")


    def finish_assessment(self):
        self.clear_frame(self.container_frame)
        content_frame = self.create_styled_frame(self.container_frame)
        content_frame.pack(pady=50, padx=50, fill="x", expand=False)

        ttk.Label(content_frame, text="🎉 Cảm ơn bạn đã hoàn thành! 🎉",
                  style="Title.TLabel").pack(pady=20)

        if self.user_responses:
            self.storage.save_responses(self.user_id, self.user_responses, "tkinter_enhanced_v1")
            ttk.Label(content_frame, text="Kết quả của bạn đã được lưu.", style="FrameSubheading.TLabel").pack(pady=10)
            ttk.Button(content_frame, text="Xem Kết Quả Phân Tích",
                       command=self.show_results_window, style="TButton").pack(pady=15, ipadx=10)
        else:
            ttk.Label(content_frame, text="Không có phản hồi nào được ghi nhận.", style="FrameSubheading.TLabel").pack(pady=10)

        buttons_frame = ttk.Frame(content_frame, style="Content.TFrame")
        buttons_frame.pack(pady=20)
        ttk.Button(buttons_frame, text="Làm lại từ đầu", command=self.setup_user_id_input, style="TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Thoát", command=self.root.quit, style="TButton").pack(side=tk.LEFT, padx=10)


    def show_results_window(self):
        results_win = tk.Toplevel(self.root)
        results_win.title(f"Kết Quả Phân Tích - {self.user_id}")
        results_win.geometry("1000x780")
        results_win.configure(bg=BG_COLOR)

        # Phải gọi phân tích ở đây để có dữ liệu mới nhất
        overall_scores = self.analyzer.calculate_overall_scores(self.user_responses)
        strengths_weaknesses = self.analyzer.identify_strengths_weaknesses(overall_scores, top_n=5)
        value_proportions = self.analyzer.analyze_value_proportions(self.user_responses)
        motivation_trends = self.analyzer.analyze_motivation_trends(self.user_responses)


        notebook = ttk.Notebook(results_win, style="TNotebook")

        tab_overview = ttk.Frame(notebook, style="TFrame", padding=15)
        notebook.add(tab_overview, text='Tổng Quan')
        canvas_overview = tk.Canvas(tab_overview, bg=BG_COLOR, highlightthickness=0)
        scrollbar_overview = ttk.Scrollbar(tab_overview, orient="vertical", command=canvas_overview.yview)
        scrollable_overview_frame = ttk.Frame(canvas_overview, style="TFrame")
        scrollable_overview_frame.bind("<Configure>", lambda e: canvas_overview.configure(scrollregion=canvas_overview.bbox("all")))
        canvas_overview.create_window((0, 0), window=scrollable_overview_frame, anchor="nw")
        canvas_overview.configure(yscrollcommand=scrollbar_overview.set)

        ttk.Label(scrollable_overview_frame, text="Bản Đồ Năng Lực & Giá Trị Chính", style="Heading.TLabel").pack(pady=(0,15), anchor="center")
        main_dims_radar = {
            k: v for k, v in overall_scores.items()
            if k in ["Linguistic Intelligence", "Logical-Mathematical Int.", "Spatial Intelligence",
                     "Bodily-Kinesthetic Int.", "Musical Intelligence", "Interpersonal Intelligence",
                     "Intrapersonal Intelligence", "Integrity", "Growth Mindset", "Social Contribution",
                     "Creativity & Innovation", "Autonomy", "Intrinsic Motivation", "Persistence",
                     "Goal Clarity", "Self-Reflection", "Emotional Awareness"]
        }
        valid_radar_scores = {k: overall_scores.get(k, 0.0) for k in main_dims_radar.keys() if isinstance(overall_scores.get(k,0.0), (int,float))}

        if valid_radar_scores:
            radar_path = self.plotter.create_radar_chart_matplotlib(valid_radar_scores, self.user_id, "")
            if radar_path and os.path.exists(radar_path):
                try:
                    img_radar_orig = Image.open(radar_path)
                    # Resize nếu cần
                    w, h = img_radar_orig.size
                    max_w, max_h = 600, 500 # Kích thước max cho radar chart
                    if w > max_w or h > max_h:
                        ratio = min(max_w/w, max_h/h)
                        img_radar = img_radar_orig.resize((int(w*ratio), int(h*ratio)), Image.Resampling.LANCZOS)
                    else:
                        img_radar = img_radar_orig

                    photo_radar = ImageTk.PhotoImage(img_radar)
                    lbl_radar = ttk.Label(scrollable_overview_frame, image=photo_radar, background=BG_COLOR)
                    lbl_radar.image = photo_radar
                    lbl_radar.pack(pady=10)
                except Exception as e:
                    print(f"Error loading radar image: {e}")
                    ttk.Label(scrollable_overview_frame, text=f"Lỗi hiển thị radar chart: {e}", background=BG_COLOR).pack()
            else: ttk.Label(scrollable_overview_frame, text="Không thể tạo/tìm thấy radar chart.", background=BG_COLOR).pack()
        else: ttk.Label(scrollable_overview_frame, text="Không đủ dữ liệu cho radar chart.", background=BG_COLOR).pack()

        ttk.Label(scrollable_overview_frame, text="Điểm Nổi Bật", style="Heading.TLabel").pack(pady=(25,10), anchor="center")
        sw_display_frame = ttk.Frame(scrollable_overview_frame, style="TFrame")
        sw_display_frame.pack(fill=tk.X, pady=10)
        strengths_frame = ttk.Labelframe(sw_display_frame, text="  Điểm Mạnh  ", style="Content.TFrame", labelanchor="n", padding=10)
        strengths_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        if strengths_weaknesses.get("strengths"):
            for item, score in strengths_weaknesses["strengths"]:
                ttk.Label(strengths_frame, text=f"• {item}: {score:.1f}", style="FrameSubheading.TLabel", padding=(0,2)).pack(anchor="w")
        else:
            ttk.Label(strengths_frame, text="Chưa xác định rõ.", style="FrameSubheading.TLabel").pack(anchor="w")
        weaknesses_frame = ttk.Labelframe(sw_display_frame, text="  Lĩnh Vực Cần Chú Ý  ", style="Content.TFrame",labelanchor="n", padding=10)
        weaknesses_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        if strengths_weaknesses.get("weaknesses"):
            for item, score in strengths_weaknesses["weaknesses"]:
                ttk.Label(weaknesses_frame, text=f"• {item}: {score:.1f}", style="FrameSubheading.TLabel", padding=(0,2)).pack(anchor="w")
        else:
            ttk.Label(weaknesses_frame, text="Chưa xác định rõ.", style="FrameSubheading.TLabel").pack(anchor="w")

        canvas_overview.pack(side="left", fill="both", expand=True)
        scrollbar_overview.pack(side="right", fill="y")

        tab_details = ttk.Frame(notebook, style="TFrame", padding=15)
        notebook.add(tab_details, text='Điểm Số Chi Tiết')
        details_text_widget = tk.Text(tab_details, wrap=tk.WORD, font=FONT_NORMAL,
                                      bg=FRAME_BG_COLOR, relief="solid", borderwidth=1, padx=10, pady=10)
        scrollbar_details = ttk.Scrollbar(tab_details, command=details_text_widget.yview)
        details_text_widget.configure(yscrollcommand=scrollbar_details.set)
        scrollbar_details.pack(side=tk.RIGHT, fill=tk.Y)
        details_text_widget.pack(fill=tk.BOTH, expand=True)
        details_content = "--- ĐIỂM SỐ TỔNG THỂ CÁC KHÍA CẠNH ---\n"
        for dim, score in sorted(overall_scores.items()):
            details_content += f"{dim}: {score:.1f}\n"
        if value_proportions:
            details_content += "\n--- TỶ LỆ GIÁ TRỊ CỐT LÕI ---\n"
            for val, prop in sorted(value_proportions.items()):
                details_content += f"{val}: {prop:.1f}%\n"
        if motivation_trends:
            details_content += "\n--- XU HƯỚNG ĐỘNG LỰC ---\n"
            for mot, score in sorted(motivation_trends.items()):
                details_content += f"{mot}: {score:.1f}\n"
        details_text_widget.insert(tk.END, details_content)
        details_text_widget.config(state=tk.DISABLED)

        open_ended_exists = any(q_info['type'] in ['open_short', 'open_long'] for q_info in self.all_questions)
        if open_ended_exists:
            tab_open_ended = ttk.Frame(notebook, style="TFrame", padding=15)
            notebook.add(tab_open_ended, text='Phản Hồi Mở')
            open_ended_text = tk.Text(tab_open_ended, wrap=tk.WORD, font=FONT_NORMAL,
                                      bg=FRAME_BG_COLOR, relief="solid", borderwidth=1, padx=10, pady=10)
            scrollbar_open = ttk.Scrollbar(tab_open_ended, command=open_ended_text.yview)
            open_ended_text.configure(yscrollcommand=scrollbar_open.set)
            scrollbar_open.pack(side=tk.RIGHT, fill=tk.Y)
            open_ended_text.pack(fill=tk.BOTH, expand=True)
            open_responses_content = ""
            has_open_answers = False
            for resp in self.user_responses:
                q_info = self.q_generator.get_question_by_id(resp['question_id'])
                if q_info and q_info['type'] in ['open_short', 'open_long'] and resp['answer']:
                    open_responses_content += f"Hỏi: {q_info['text']}\nĐáp: {resp['answer']}\n\n"
                    has_open_answers = True
            open_ended_text.insert(tk.END, open_responses_content if has_open_answers else "Không có phản hồi cho câu hỏi mở.")
            open_ended_text.config(state=tk.DISABLED)

        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        def save_html_report_action():
            # Đảm bảo các biến này được cập nhật từ phân tích mới nhất
            current_overall_scores = self.analyzer.calculate_overall_scores(self.user_responses)
            current_sw = self.analyzer.identify_strengths_weaknesses(current_overall_scores, top_n=5)
            current_values = self.analyzer.analyze_value_proportions(self.user_responses)
            current_motivation = self.analyzer.analyze_motivation_trends(self.user_responses)

            open_ended_formatted = []
            for resp in self.user_responses:
                q_info = self.q_generator.get_question_by_id(resp['question_id'])
                if q_info and q_info['type'] in ['open_short', 'open_long'] and resp['answer']:
                    open_ended_formatted.append({"question_text": q_info['text'], "answer": resp['answer']})

            chart_paths_for_report_abs = {}
            if valid_radar_scores:
                radar_file_for_report = self.plotter.create_radar_chart_matplotlib(valid_radar_scores, self.user_id, "")
                if radar_file_for_report: # Plotter trả về None nếu lỗi
                     chart_paths_for_report_abs["radar_png"] = radar_file_for_report # Đã là abs path từ plotter

            # Tạo thêm Bar Chart và Pie Chart cho báo cáo nếu muốn (giả sử đã có trong Plotter)
            if current_sw["strengths"]:
                strengths_data_report = {item: score for item, score in current_sw["strengths"]}
                bar_strengths_file = self.plotter.create_bar_chart_matplotlib(strengths_data_report, self.user_id, "Điểm mạnh")
                if bar_strengths_file: chart_paths_for_report_abs["bar_strengths_png"] = bar_strengths_file

            if current_values:
                pie_values_file = self.plotter.create_pie_chart_matplotlib(current_values, self.user_id, "Tỷ lệ Giá trị")
                if pie_values_file: chart_paths_for_report_abs["pie_values_png"] = pie_values_file

            if current_motivation:
                pie_motivation_file = self.plotter.create_pie_chart_matplotlib(current_motivation, self.user_id, "Xu hướng Động lực")
                if pie_motivation_file: chart_paths_for_report_abs["pie_motivation_png"] = pie_motivation_file


            html_path_result = self.reporter.generate_html_report(
                self.user_id, current_overall_scores, current_sw,
                current_values, current_motivation, open_ended_formatted,
                chart_paths_for_report_abs # Truyền dict chứa đường dẫn tuyệt đối
            )
            if html_path_result and os.path.exists(html_path_result):
                abs_path_html = os.path.abspath(html_path_result)
                messagebox.showinfo("Thành Công", f"Báo cáo HTML đã lưu tại:\n{abs_path_html}")
                if messagebox.askyesno("Mở Báo Cáo", "Bạn có muốn mở file báo cáo vừa lưu trong trình duyệt không?"):
                    try:
                        uri_path = f"file:///{abs_path_html.replace(os.sep, '/')}"
                        webbrowser.open(uri_path)
                    except Exception as e_open:
                        messagebox.showerror("Lỗi Mở File", f"Không thể tự động mở báo cáo: {e_open}")
            else:
                messagebox.showerror("Lỗi", "Không thể tạo báo cáo HTML.")

        ttk.Button(results_win, text="Lưu Báo Cáo HTML", command=save_html_report_action, style="TButton").pack(pady=15, ipadx=10)