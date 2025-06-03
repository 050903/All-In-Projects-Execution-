# self_assessment_system/main.py
import tkinter as tk
import sys
import os

# Logic để đảm bảo sys.path đúng khi chạy từ các vị trí khác nhau (ví dụ khi đóng gói)
# Cách đơn giản nhất là giả định script này nằm trong thư mục gốc của dự án
# và các thư mục con 'ui', 'core' được truy cập trực tiếp.

try:
    from ui.tkinter_app import EnhancedTkinterApp
except ModuleNotFoundError:
    # Thử thêm thư mục cha vào sys.path nếu đang chạy từ thư mục con (vd: ui)
    # Điều này ít xảy ra nếu bạn chạy từ thư mục gốc của dự án.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from ui.tkinter_app import EnhancedTkinterApp
    except ModuleNotFoundError as e_inner:
        print(f"Lỗi import nghiêm trọng sau khi điều chỉnh sys.path: {e_inner}")
        print("Vui lòng đảm bảo bạn chạy script từ thư mục gốc 'self_assessment_system'.")
        sys.exit(1)
except ImportError as e:
    print(f"Lỗi import: Không thể tìm thấy module ui.tkinter_app hoặc các module phụ thuộc: {e}")
    print(f"Current sys.path: {sys.path}")
    print("Đảm bảo bạn đang chạy script từ thư mục gốc của dự án (self_assessment_system), "
          "và các file __init__.py tồn tại trong các thư mục con (ui, core, etc.).")
    sys.exit(1)


def main_tkinter():
    # Kiểm tra file questions.json trước khi khởi tạo app
    # Đường dẫn tương đối từ vị trí file main.py
    questions_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'questions.json')

    if not os.path.exists(questions_file_path):
        try:
            # Thử tạo cửa sổ lỗi Tkinter một cách an toàn
            root_error_check = tk.Tk()
            root_error_check.withdraw()
            from tkinter import messagebox # Import cục bộ để tránh lỗi nếu Tk chưa sẵn sàng
            messagebox.showerror("Lỗi Nghiêm Trọng",
                                 f"Không tìm thấy file câu hỏi cần thiết:\n{questions_file_path}\n\n"
                                 "Ứng dụng không thể khởi động. Vui lòng kiểm tra lại cấu trúc thư mục và file 'assets/questions.json'.")
            root_error_check.destroy()
        except tk.TclError: # Nếu Tkinter không thể khởi tạo (ví dụ: không có DISPLAY)
            print(f"LỖI NGHIÊM TRỌNG: Không tìm thấy file câu hỏi: {questions_file_path}")
            print("Ứng dụng không thể khởi động.")
        sys.exit(1)

    root = tk.Tk()
    app = EnhancedTkinterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main_tkinter()