# self_assessment_system/visualization/plotter.py
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple # Đảm bảo import Tuple nếu dùng
import os

class Plotter:
    def __init__(self, output_dir: str = "output_charts_tkinter_enhanced"):
        # Tạo đường dẫn tuyệt đối cho thư mục output ngay từ đầu
        # Giả sử script chạy từ thư mục gốc của dự án, nơi chứa thư mục output_dir
        self.base_output_dir = os.path.abspath(os.path.join(os.getcwd(), output_dir))
        if not os.path.exists(self.base_output_dir):
            os.makedirs(self.base_output_dir)
        print(f"Thư mục lưu biểu đồ plotter: {self.base_output_dir}")


    def create_radar_chart_matplotlib(self,
                                      scores: Dict[str, float],
                                      user_id: str,
                                      title: str = "Bản đồ năng lực cá nhân") -> str | None:
        if not scores:
            print("Cảnh báo (Plotter): Không có dữ liệu điểm để vẽ Radar Chart.")
            return None

        labels = np.array(list(scores.keys()))
        stats = np.array(list(scores.values())) # stats sẽ là giá trị từ dict
        num_vars = len(labels)

        if num_vars < 3: # Radar chart cần ít nhất 3 trục
            print(f"Cảnh báo (Plotter): Radar chart cần ít nhất 3 khía cạnh để vẽ, hiện có {num_vars}.")
            return None


        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        # Đảm bảo stats là numpy array trước khi concatenate
        stats_np = np.array(stats, dtype=float)
        stats_closed = np.concatenate((stats_np, [stats_np[0]]))
        angles_closed = angles + [angles[0]]

        fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True)) # Tăng kích thước một chút
        ax.plot(angles_closed, stats_closed, color='#007ACC', linewidth=2, linestyle='solid', marker='o', markersize=5) # Thêm marker
        ax.fill(angles_closed, stats_closed, color='#007ACC', alpha=0.25)

        # Nhãn cho các trục
        ax.set_thetagrids(np.degrees(angles), labels, fontsize=10, color='#333', wrap=True) # Thêm wrap cho label dài

        # Đặt các mức trên trục R
        max_score_val = 5.0 # Mặc định
        if stats_np.size > 0 :
            max_in_stats = np.max(stats_np) # Không cần bỏ điểm cuối vì stats_np là gốc
            if not np.isnan(max_in_stats) and max_in_stats > 0: # Xử lý NaN
                 max_score_val = np.ceil(max_in_stats) if max_in_stats > 5.0 else 5.0

        # Đảm bảo các tick hợp lý, ví dụ mỗi 1 đơn vị
        yticks = np.arange(0, max_score_val + 1, 1)
        ax.set_yticks(yticks)
        ax.set_yticklabels([str(int(y)) for y in yticks], fontsize=9, color='#555') # Hiển thị số nguyên
        ax.set_ylim(0, max_score_val)

        if title:
            ax.set_title(title, va='bottom', fontsize=15, color='#005A9E', y=1.1) # Điều chỉnh y để title không đè
        ax.grid(True, linestyle='--', alpha=0.6, color='#ccc')

        # Làm sạch user_id và title để tạo tên file an toàn
        safe_user_id = "".join(c if c.isalnum() or c in ('_') else '' for c in str(user_id)).rstrip('_')
        safe_title_filename = "".join(c if c.isalnum() or c == '_' else '' for c in title.lower().replace(' ','_').replace(':','').replace('/',''))[:30]
        filename = f"radar_matplotlib_{safe_user_id}_{safe_title_filename}.png"
        filepath = os.path.join(self.base_output_dir, filename)

        try:
            plt.tight_layout() # Đảm bảo các label không bị cắt
            plt.savefig(filepath, dpi=120, bbox_inches='tight') # Tăng dpi một chút
            plt.close(fig)
            print(f"Đã lưu Radar Chart Matplotlib: {filepath}")
            return os.path.abspath(filepath)
        except Exception as e:
            print(f"Lỗi khi lưu Radar Chart Matplotlib: {e}")
            plt.close(fig)
            return None


    def create_bar_chart_matplotlib(self,
                                    data: Dict[str, float],
                                    user_id: str,
                                    title: str,
                                    xlabel: str = "Khía cạnh",
                                    ylabel: str = "Điểm số") -> str | None:
        if not data:
            print("Cảnh báo (Plotter): Không có dữ liệu để vẽ Bar Chart.")
            return None

        # Sắp xếp data theo giá trị giảm dần để dễ nhìn hơn (tùy chọn)
        # sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
        # categories = list(sorted_data.keys())
        # values = list(sorted_data.values())
        categories = list(data.keys())
        values = [float(v) if v is not None else 0.0 for v in data.values()] # Xử lý None

        fig, ax = plt.subplots(figsize=(max(7, len(categories) * 0.7), 6)) # Điều chỉnh figsize
        bars = ax.bar(categories, values, color='#007ACC', alpha=0.85, width=0.7)
        ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
        ax.set_ylabel(ylabel, fontsize=11, labelpad=10)
        ax.set_title(title, fontsize=15, color='#005A9E', pad=15) # Thêm padding

        # Xoay và căn chỉnh nhãn trục X
        ax.tick_params(axis='x', rotation=40, labelsize=9.5) # labelsize thay vì fontsize
        plt.setp(ax.get_xticklabels(), ha="right", rotation_mode="anchor") # Căn chỉnh ngang
        ax.tick_params(axis='y', labelsize=9.5)

        ax.grid(True, axis='y', linestyle=':', alpha=0.7, color='#bbb') # Đổi linestyle
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#ccc')
        ax.spines['bottom'].set_color('#ccc')

        # Thêm giá trị trên đầu mỗi cột bar
        max_val_for_text = max(values, default=1.0) # Để tránh lỗi nếu values rỗng hoặc toàn 0
        if max_val_for_text == 0: max_val_for_text = 1.0 # Tránh chia cho 0

        for bar in bars:
            yval = bar.get_height()
            text_y_pos = yval + 0.02 * max_val_for_text # Vị trí text dựa trên max_val
            text_color = '#333'

            # Nếu thanh quá ngắn, đặt text bên ngoài và đảm bảo nó không bị cắt ở đáy
            if yval < 0.1 * max_val_for_text : # Ngưỡng cho thanh ngắn
                text_y_pos = yval + 0.01 * max_val_for_text # Gần hơn một chút
                # va = 'bottom' # Có thể cần thiết
            elif yval > 0.95 * ax.get_ylim()[1]: # Nếu quá gần đỉnh, cân nhắc đặt bên trong
                 text_y_pos = yval - 0.03 * max_val_for_text
                 text_color = 'white'


            plt.text(bar.get_x() + bar.get_width()/2.0, text_y_pos, f'{yval:.1f}',
                     ha='center', va='bottom', fontsize=8.5, color=text_color, weight='medium')

        # Đảm bảo có khoảng trống ở trên cùng cho text
        ax.set_ylim(0, ax.get_ylim()[1] * 1.1)


        safe_user_id = "".join(c if c.isalnum() or c == '_' else '' for c in str(user_id)).rstrip('_')
        safe_title_filename = "".join(c if c.isalnum() or c == '_' else '' for c in title.lower().replace(' ','_').replace(':','').replace('/',''))[:30]
        filename = f"bar_chart_matplotlib_{safe_user_id}_{safe_title_filename}.png"
        filepath = os.path.join(self.base_output_dir, filename)

        try:
            plt.tight_layout(pad=1.5) # Thêm padding cho tight_layout
            plt.savefig(filepath, dpi=120)
            plt.close(fig)
            print(f"Đã lưu Bar Chart Matplotlib: {filepath}")
            return os.path.abspath(filepath)
        except Exception as e:
            print(f"Lỗi khi lưu Bar Chart Matplotlib: {e}")
            plt.close(fig)
            return None


    def create_pie_chart_matplotlib(self,
                                    data: Dict[str, float],
                                    user_id: str,
                                    title: str) -> str | None:
        # Lọc bỏ các giá trị không dương hoặc quá nhỏ để tránh lỗi hoặc biểu đồ xấu
        valid_data = {k: v for k, v in data.items() if isinstance(v, (int, float)) and v > 0.01} # Ngưỡng nhỏ

        if not valid_data or sum(valid_data.values()) == 0:
            print("Cảnh báo (Plotter): Không có dữ liệu hợp lệ (giá trị > 0) để vẽ Pie Chart.")
            return None

        labels = list(valid_data.keys())
        sizes = list(valid_data.values())

        num_labels = len(labels)
        if num_labels <= 7:
            colors = plt.cm.Pastel1(np.arange(num_labels)/float(num_labels)) # Màu Pastel1 cho ít mục
        elif num_labels <= 12:
            colors = plt.cm.Set3(np.arange(num_labels)/float(num_labels)) # Màu Set3
        else: # Nhiều mục thì dùng viridis hoặc các colormap khác
            colors = plt.cm.viridis(np.linspace(0.1, 0.9, num_labels))


        fig, ax = plt.subplots(figsize=(7.5, 6.5)) # Điều chỉnh figsize
        # explode_factor = 0.03 # Tách nhẹ các múi
        # explode = [explode_factor] * num_labels if num_labels > 1 else [0] # Chỉ explode nếu có nhiều hơn 1 múi
        explode = None # Bỏ explode nếu không muốn

        wedges, texts, autotexts = ax.pie(sizes,
                                          explode=explode,
                                          # labels=labels if num_labels <= 6 else None, # Chỉ hiển thị label trên pie nếu ít
                                          autopct=lambda p: f'{p:.1f}%' if p > 3 else '', # Chỉ hiện % nếu lớn hơn 3%
                                          shadow=False, startangle=140, colors=colors,
                                          wedgeprops={'edgecolor': 'white', 'linewidth': 0.7},
                                          pctdistance=0.8 if num_labels <=6 else 0.7, # Điều chỉnh pctdistance
                                          labeldistance=1.05 if num_labels <=6 else None
                                          )

        plt.setp(autotexts, size=9, weight="bold", color="black") # Thử màu đen cho %
        if num_labels <= 6: # Điều chỉnh label texts nếu hiển thị trực tiếp
            plt.setp(texts, size=10, color='#444')

        ax.set_title(title, fontsize=15, color='#005A9E', pad=20)
        ax.axis('equal')

        # Thêm legend nếu có nhiều hơn 6 mục hoặc nếu muốn
        if num_labels > 0 : # Luôn thêm legend để nhất quán, hoặc có thể là num_labels > 6
             # Định dạng legend
            legend_labels = [f'{l} ({s/sum(sizes)*100:.1f}%)' for l, s in zip(labels, sizes)]
            ax.legend(wedges, legend_labels,
                      title="Thành phần",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1), # Đặt legend bên phải
                      fontsize=9.5, title_fontsize='10')


        safe_user_id = "".join(c if c.isalnum() or c == '_' else '' for c in str(user_id)).rstrip('_')
        safe_title_filename = "".join(c if c.isalnum() or c == '_' else '' for c in title.lower().replace(' ','_').replace(':','').replace('/',''))[:30]
        filename = f"pie_chart_matplotlib_{safe_user_id}_{safe_title_filename}.png"
        filepath = os.path.join(self.base_output_dir, filename)

        try:
            plt.tight_layout(rect=[0, 0, 0.85, 1] if num_labels > 0 else None) # Điều chỉnh rect để có chỗ cho legend
            plt.savefig(filepath, dpi=120)
            plt.close(fig)
            print(f"Đã lưu Pie Chart Matplotlib: {filepath}")
            return os.path.abspath(filepath)
        except Exception as e:
            print(f"Lỗi khi lưu Pie Chart Matplotlib: {e}")
            plt.close(fig)
            return None

# --- Test Plotter (để chạy riêng file này) ---
if __name__ == '__main__':
    # Tạo thư mục test nếu chưa có, giả sử chạy từ thư mục visualization
    test_output_dir = os.path.join(os.path.dirname(__file__), "test_plotter_output")
    plotter_test = Plotter(output_dir=test_output_dir)
    sample_user_id_test = "TestUser123"

    print(f"\n--- Test Radar Chart ---")
    radar_scores_test = {
        "Logic": 4.5, "Ngôn ngữ": 3.0, "Không gian": 4.0,
        "Vận động": 2.5, "Âm nhạc": 3.5, "Tương tác Xã Hội": 4.2, "Nội tâm": 3.8,
        "Sáng Tạo": 4.1, "Kiên Trì": 3.3
    }
    if len(radar_scores_test) >=3:
        radar_path_test = plotter_test.create_radar_chart_matplotlib(radar_scores_test, sample_user_id_test, "Bản Đồ Kỹ Năng Tổng Hợp")
        if radar_path_test: print(f"Radar chart test đã lưu tại: {radar_path_test}")
    else:
        print("Không đủ điểm cho radar chart test")

    print(f"\n--- Test Bar Chart ---")
    bar_data_test = {"Điểm Mạnh A": 4.5, "Điểm Mạnh B": 4.0, "Cần Cải Thiện X": 2.0, "Kỹ Năng Y": 3.5}
    bar_path_test = plotter_test.create_bar_chart_matplotlib(bar_data_test, sample_user_id_test, "Phân Tích Điểm Mạnh Yếu", "Khía Cạnh", "Mức Độ")
    if bar_path_test: print(f"Bar chart test đã lưu tại: {bar_path_test}")

    print(f"\n--- Test Pie Chart ---")
    pie_data_test = {"Giá Trị Chính": 40, "Giá Trị Phụ": 30, "Giá Trị Khác": 20, "Ưu Tiên Thấp": 10}
    pie_path_test = plotter_test.create_pie_chart_matplotlib(pie_data_test, sample_user_id_test, "Phân Bổ Giá Trị Ưu Tiên")
    if pie_path_test: print(f"Pie chart test đã lưu tại: {pie_path_test}")

    pie_data_motivation = {"Nội tại": 4.2, "Ngoại tại": 3.1, "Áp lực": 1.5}
    pie_motivation_path = plotter_test.create_pie_chart_matplotlib(pie_data_motivation, sample_user_id_test, "Xu Hướng Động Lực Chính")
    if pie_motivation_path: print(f"Pie motivation chart test đã lưu tại: {pie_motivation_path}")