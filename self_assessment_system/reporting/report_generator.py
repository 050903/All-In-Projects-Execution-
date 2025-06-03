# self_assessment_system/reporting/report_generator.py
import os
import datetime
from typing import Dict, List, Any, Tuple

class ReportGenerator:
    def __init__(self, output_dir: str = "output_reports_tkinter_enhanced"):
        # Tạo đường dẫn tuyệt đối cho thư mục output của báo cáo
        self.base_report_dir = os.path.abspath(os.path.join(os.getcwd(), output_dir))
        if not os.path.exists(self.base_report_dir):
            os.makedirs(self.base_report_dir)

    def _format_strengths_weaknesses(self, sw_data: Dict[str, List[Tuple[str, float]]]) -> str:
        html_output = ""
        if sw_data.get("strengths"):
            html_output += "<h3>Điểm mạnh nổi bật:</h3><ul>"
            for item, score in sw_data["strengths"]:
                html_output += f"<li>{item}: {score:.1f}</li>"
            html_output += "</ul>"
        else:
            html_output += "<p>Chưa xác định rõ điểm mạnh.</p>"


        if sw_data.get("weaknesses"):
            html_output += "<h3>Lĩnh vực cần chú ý/cải thiện:</h3><ul>"
            for item, score in sw_data["weaknesses"]:
                html_output += f"<li>{item}: {score:.1f}</li>"
            html_output += "</ul>"
        else:
            html_output += "<p>Chưa xác định rõ lĩnh vực cần cải thiện.</p>"
        return html_output

    def _format_dict_to_html_list(self, data: Dict[str, Any], title: str, unit: str = "") -> str:
        if not data:
            return f"<h3>{title}:</h3><p>Không có dữ liệu.</p>"
        html_output = f"<h3>{title}:</h3><ul>"
        for key, value in sorted(data.items()): # Sắp xếp để nhất quán
            display_value = f"{value:.1f}{unit}" if isinstance(value, float) else f"{value}{unit}"
            html_output += f"<li>{key}: {display_value}</li>"
        html_output += "</ul>"
        return html_output

    def generate_html_report(self,
                             user_id: str,
                             overall_scores: Dict[str, float],
                             strengths_weaknesses: Dict[str, List[Tuple[str, float]]],
                             value_proportions: Dict[str, float],
                             motivation_trends: Dict[str, float],
                             open_ended_responses: List[Dict[str, str]],
                             chart_paths_absolute: Dict[str, str | None]
                            ) -> str | None:
        report_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_filename_base = f"report_{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
        report_filepath_absolute = os.path.join(self.base_report_dir, f"{report_filename_base}.html")

        chart_paths_relative = {}
        for key, abs_chart_path in chart_paths_absolute.items():
            if abs_chart_path and os.path.exists(os.path.abspath(abs_chart_path)): # Đảm bảo path truyền vào cũng tuyệt đối
                try:
                    # Đường dẫn tương đối từ thư mục chứa HTML đến file ảnh
                    relative_path = os.path.relpath(os.path.abspath(abs_chart_path), start=self.base_report_dir)
                    chart_paths_relative[key] = relative_path.replace(os.sep, '/')
                except ValueError:
                    chart_paths_relative[key] = None
                    print(f"Cảnh báo: Không thể tạo đường dẫn tương đối cho {abs_chart_path} từ {self.base_report_dir}.")
            else:
                chart_paths_relative[key] = None

        radar_src = chart_paths_relative.get("radar_png")
        bar_strengths_src = chart_paths_relative.get("bar_strengths_png") # Cần tạo biểu đồ này nếu muốn dùng
        pie_values_src = chart_paths_relative.get("pie_values_png")
        pie_motivation_src = chart_paths_relative.get("pie_motivation_png")


        html_content = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Báo cáo Tự Đánh Giá Cá Nhân - {user_id}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding:0; line-height: 1.6; background-color: #f8f9fa; color: #333; }}
                .container {{ max-width: 960px; margin: 30px auto; background: #ffffff; padding: 20px 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
                header {{ text-align: center; margin-bottom: 30px; border-bottom: 1px solid #e0e0e0; padding-bottom: 20px; }}
                header h1 {{ color: #007ACC; font-size: 2.2em; margin-bottom: 5px;}}
                header p {{ font-size: 1em; color: #555; }}
                .section {{ margin-bottom: 35px; padding: 20px; background-color:#fdfdfd; border: 1px solid #efefef; border-radius:5px;}}
                .section h2 {{ color: #005A9E; font-size: 1.6em; margin-top: 0; border-bottom: 2px solid #007ACC; padding-bottom: 8px; }}
                .section h3 {{ color: #333; font-size: 1.3em; margin-top: 20px; margin-bottom:10px; border-left: 3px solid #007ACC; padding-left:10px;}}
                .chart-container {{ margin: 20px auto; text-align: center; padding:15px; background: #f9f9f9; border-radius: 5px; }}
                .chart-container img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
                ul {{ list-style-type: none; padding-left: 0; }}
                li {{ background-color: #f9f9f9; margin-bottom: 8px; padding: 10px; border-left: 3px solid #007ACC; border-radius:3px; }}
                li strong {{ color: #005A9E; }}
                .open-response-item {{ margin-bottom: 15px; }}
                .open-response-item .question-text {{ font-weight: bold; color: #444; margin-bottom:5px; }}
                .open-response-item .answer-text {{ padding-left: 15px; font-style: italic; color:#555;}}
                footer {{ text-align: center; margin-top: 40px; padding: 20px 0; font-size: 0.9em; color: #777; border-top: 1px solid #e0e0e0;}}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Báo Cáo Tự Đánh Giá Cá Nhân</h1>
                    <p><strong>Người thực hiện:</strong> {user_id}</p>
                    <p><strong>Ngày tạo báo cáo:</strong> {report_timestamp}</p>
                </header>

                <div class="section">
                    <h2>Tổng Quan Năng Lực & Các Khía Cạnh Chính</h2>
                    <div class="chart-container">
                        <h3>Bản đồ các khía cạnh</h3>
                        {f'<img src="{radar_src}" alt="Radar Chart">' if radar_src else "<p>Không có biểu đồ radar.</p>"}
                    </div>
                    {self._format_dict_to_html_list(overall_scores, "Điểm số chi tiết các khía cạnh")}
                </div>

                <div class="section">
                    <h2>Điểm Nổi Bật</h2>
                    {self._format_strengths_weaknesses(strengths_weaknesses)}
                    {f'''<div class="chart-container">
                            <h3>Biểu đồ điểm mạnh (ví dụ)</h3>
                            {f'<img src="{bar_strengths_src}" alt="Bar Chart Strengths">' if bar_strengths_src else "<p>Chưa có biểu đồ điểm mạnh.</p>"}
                        </div>''' if bar_strengths_src else ""}
                </div>

                <div class="section">
                    <h2>Phân Tích Giá Trị Cốt Lõi</h2>
                    {self._format_dict_to_html_list(value_proportions, "Tỷ lệ các giá trị được ưu tiên", unit="%")}
                    {f'''<div class="chart-container">
                            <h3>Biểu đồ tỷ lệ giá trị</h3>
                            {f'<img src="{pie_values_src}" alt="Pie Chart Values">' if pie_values_src else "<p>Chưa có biểu đồ giá trị.</p>"}
                        </div>''' if pie_values_src else ""}
                </div>

                <div class="section">
                    <h2>Phân Tích Xu Hướng Động Lực</h2>
                    {self._format_dict_to_html_list(motivation_trends, "Điểm số các loại động lực")}
                    {f'''<div class="chart-container">
                            <h3>Biểu đồ xu hướng động lực</h3>
                            {f'<img src="{pie_motivation_src}" alt="Pie Chart Motivation">' if pie_motivation_src else "<p>Chưa có biểu đồ động lực.</p>"}
                        </div>''' if pie_motivation_src else ""}
                </div>
        """
        if open_ended_responses:
            html_content += """
                <div class="section">
                    <h2>Phản Hồi Câu Hỏi Mở</h2>
            """
            for resp in open_ended_responses:
                html_content += f"""
                    <div class="open-response-item">
                        <p class="question-text">{resp['question_text']}</p>
                        <p class="answer-text">{resp['answer']}</p>
                    </div>
                """
            html_content += "</div>"
        else:
            html_content += """
                <div class="section">
                    <h2>Phản Hồi Câu Hỏi Mở</h2>
                    <p>Không có phản hồi cho câu hỏi mở.</p>
                </div>
            """

        html_content += """
                <footer>
                    <p>© {datetime.date.today().year} Hệ Thống Tự Đánh Giá Cá Nhân InsightMe</p>
                </footer>
            </div>
        </body>
        </html>
        """

        try:
            with open(report_filepath_absolute, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Đã tạo báo cáo HTML: {report_filepath_absolute}")
            return report_filepath_absolute
        except IOError as e:
            print(f"Lỗi khi tạo báo cáo HTML: {e}")
            return None