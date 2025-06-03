import json
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# --- PHẦN 0: CẤU HÌNH FONT CHO MATPLOTLIB (Đảm bảo hiển thị tiếng Việt) ---
# Bạn có thể cần cài đặt font hỗ trợ tiếng Việt vào hệ thống
# và thay 'Arial' bằng tên font đó nếu Arial không có sẵn hoặc không hỗ trợ tốt.
plt.rcParams['font.family'] = 'Arial' # Hoặc 'Tahoma', 'Times New Roman' nếu có
plt.rcParams['axes.unicode_minus'] = False # Hiển thị dấu trừ đúng cách

# --- PHẦN 1: KHỞI TẠO CÂU HỎI (Mở rộng lên ~50 câu) ---
def khoi_tao_cau_hoi():
    """
    Hàm này khởi tạo một danh sách các câu hỏi cho từng khía cạnh đánh giá.
    Mỗi câu hỏi có một ID, nội dung, và loại (khía cạnh).
    Người dùng sẽ trả lời trên thang điểm Likert (ví dụ: 1-5).
    """
    cau_hoi = {
        "gia_tri_cot_loi": [
            # Hiện có 5, thêm 5
            {"id": "gtcl_1", "cau_hoi": "Bạn có thường xuyên ưu tiên sự trung thực trong mọi hành động không?", "loai": "Trung thực"},
            {"id": "gtcl_2", "cau_hoi": "Sự công bằng có phải là một yếu tố quan trọng trong các quyết định của bạn không?", "loai": "Công bằng"},
            {"id": "gtcl_3", "cau_hoi": "Bạn có đề cao sự phát triển cá nhân và học hỏi liên tục không?", "loai": "Phát triển cá nhân"},
            {"id": "gtcl_4", "cau_hoi": "Lòng trắc ẩn và sự đồng cảm có vai trò như thế nào đối với bạn?", "loai": "Trắc ẩn & Đồng cảm"},
            {"id": "gtcl_5", "cau_hoi": "Bạn có coi trọng sự tự do và độc lập trong suy nghĩ và hành động không?", "loai": "Tự do & Độc lập"},
            {"id": "gtcl_6", "cau_hoi": "Bạn có luôn chịu trách nhiệm về hành động và quyết định của mình không?", "loai": "Trách nhiệm"},
            {"id": "gtcl_7", "cau_hoi": "Bạn có tôn trọng sự khác biệt và quan điểm của người khác không?", "loai": "Tôn trọng"},
            {"id": "gtcl_8", "cau_hoi": "Sự sáng tạo và đổi mới có ý nghĩa như thế nào trong công việc/cuộc sống của bạn?", "loai": "Sáng tạo & Đổi mới"},
            {"id": "gtcl_9", "cau_hoi": "Bạn có duy trì kỷ luật cá nhân để đạt được mục tiêu đề ra không?", "loai": "Kỷ luật"},
            {"id": "gtcl_10", "cau_hoi": "Bạn có mong muốn đóng góp cho cộng đồng hoặc những mục đích lớn hơn bản thân không?", "loai": "Đóng góp"},
        ],
        "tri_thong_minh_noi_troi": [
            # Hiện có 8, thêm 2 để chi tiết hơn
            {"id": "ttm_1", "cau_hoi": "Bạn có khả năng diễn đạt ý tưởng một cách rõ ràng và mạch lạc bằng lời nói hoặc văn viết không (Ngôn ngữ)?", "loai": "Ngôn ngữ"},
            {"id": "ttm_2", "cau_hoi": "Bạn có dễ dàng nhận biết các quy luật, giải quyết vấn đề logic và làm việc với các con số không (Logic-Toán học)?", "loai": "Logic-Toán học"},
            {"id": "ttm_3", "cau_hoi": "Bạn có nhạy cảm với âm thanh, nhịp điệu và có khả năng cảm thụ âm nhạc tốt không (Âm nhạc)?", "loai": "Âm nhạc"},
            {"id": "ttm_4", "cau_hoi": "Bạn có khả năng cảm nhận không gian, hình dung các đối tượng 3D và có năng khiếu về nghệ thuật thị giác không (Không gian)?", "loai": "Không gian"},
            {"id": "ttm_5", "cau_hoi": "Bạn có khả năng sử dụng cơ thể một cách khéo léo để giải quyết vấn đề hoặc tạo ra sản phẩm (Vận động cơ thể)?", "loai": "Vận động cơ thể"},
            {"id": "ttm_6", "cau_hoi": "Bạn có khả năng thấu hiểu và tương tác hiệu quả với người khác không (Tương tác cá nhân)?", "loai": "Tương tác cá nhân"},
            {"id": "ttm_7", "cau_hoi": "Bạn có khả năng tự nhận thức rõ về bản thân, điểm mạnh, điểm yếu và cảm xúc của mình không (Nội tâm)?", "loai": "Nội tâm"},
            {"id": "ttm_8", "cau_hoi": "Bạn có yêu thích thiên nhiên, dễ dàng nhận biết và phân loại các loài động thực vật không (Thiên nhiên)?", "loai": "Thiên nhiên"},
            {"id": "ttm_9", "cau_hoi": "Bạn có thích tranh luận, phân tích các vấn đề từ nhiều góc độ và tìm ra luận điểm thuyết phục không (Ngôn ngữ - mở rộng)?", "loai": "Ngôn ngữ"},
            {"id": "ttm_10", "cau_hoi": "Bạn có thường tìm kiếm các mô hình, cấu trúc ẩn sau các hiện tượng hoặc thông tin không (Logic-Toán học - mở rộng)?", "loai": "Logic-Toán học"},
        ],
        "dong_luc_hoc_tap_hanh_dong": [
            # Hiện có 5, thêm 5
            {"id": "dl_1", "cau_hoi": "Bạn có cảm thấy hứng thú khi đối mặt với những thử thách học tập mới không?", "loai": "Động lực học tập (Thử thách)"},
            {"id": "dl_2", "cau_hoi": "Mục tiêu rõ ràng có giúp bạn duy trì động lực trong công việc và học tập không?", "loai": "Động lực hành động (Mục tiêu)"},
            {"id": "dl_3", "cau_hoi": "Sự công nhận từ người khác có phải là yếu tố thúc đẩy bạn không?", "loai": "Động lực bên ngoài (Công nhận)"},
            {"id": "dl_4", "cau_hoi": "Bạn có thường tự đặt ra các tiêu chuẩn cao cho bản thân không?", "loai": "Động lực bên trong (Tiêu chuẩn cao)"},
            {"id": "dl_5", "cau_hoi": "Khi gặp khó khăn, bạn có xu hướng kiên trì hay dễ dàng từ bỏ?", "loai": "Động lực duy trì (Kiên trì)"},
            {"id": "dl_6", "cau_hoi": "Bạn có tin rằng nỗ lực có thể cải thiện khả năng của mình (Tư duy phát triển) không?", "loai": "Động lực bên trong (Tư duy phát triển)"},
            {"id": "dl_7", "cau_hoi": "Nỗi sợ thất bại có thường cản trở bạn thử những điều mới không?", "loai": "Rào cản động lực (Sợ thất bại)"}, # Điểm thấp hơn ở câu này có thể là tốt
            {"id": "dl_8", "cau_hoi": "Bạn có tìm thấy niềm vui trong chính quá trình học tập/làm việc, thay vì chỉ kết quả cuối cùng không?", "loai": "Động lực bên trong (Niềm vui quá trình)"},
            {"id": "dl_9", "cau_hoi": "Phần thưởng (tiền bạc, điểm số) có phải là động lực chính yếu của bạn không?", "loai": "Động lực bên ngoài (Phần thưởng)"},
            {"id": "dl_10", "cau_hoi": "Bạn có chủ động tìm kiếm cơ hội để học hỏi và phát triển kỹ năng không?", "loai": "Động lực học tập (Chủ động)"},
        ],
        "muc_tieu_ca_nhan": [
            # Hiện có 3, thêm 7
            {"id": "mt_1", "cau_hoi": "Bạn có xác định rõ ràng các mục tiêu ngắn hạn (trong 1 năm tới) của mình không?", "loai": "Mục tiêu ngắn hạn (Rõ ràng)"},
            {"id": "mt_2", "cau_hoi": "Bạn có kế hoạch cụ thể để đạt được các mục tiêu dài hạn (3-5 năm) không?", "loai": "Mục tiêu dài hạn (Kế hoạch)"},
            {"id": "mt_3", "cau_hoi": "Bạn có thường xuyên xem xét và điều chỉnh mục tiêu cá nhân của mình không?", "loai": "Quản lý mục tiêu (Xem xét & Điều chỉnh)"},
            {"id": "mt_4", "cau_hoi": "Các mục tiêu của bạn có cụ thể, đo lường được, khả thi, liên quan và có thời hạn (SMART) không?", "loai": "Mục tiêu SMART"},
            {"id": "mt_5", "cau_hoi": "Mục tiêu của bạn có phù hợp với giá trị cốt lõi của bạn không?", "loai": "Mục tiêu (Phù hợp giá trị)"},
            {"id": "mt_6", "cau_hoi": "Bạn có chia nhỏ mục tiêu lớn thành các bước hành động nhỏ hơn không?", "loai": "Mục tiêu (Chia nhỏ hành động)"},
            {"id": "mt_7", "cau_hoi": "Bạn có hình dung rõ ràng về kết quả khi đạt được mục tiêu không?", "loai": "Mục tiêu (Hình dung kết quả)"},
            {"id": "mt_8", "cau_hoi": "Bạn có sẵn sàng thay đổi kế hoạch khi gặp trở ngại không lường trước không?", "loai": "Mục tiêu (Linh hoạt)"},
            {"id": "mt_9", "cau_hoi": "Bạn có theo dõi tiến độ thực hiện mục tiêu của mình không?", "loai": "Quản lý mục tiêu (Theo dõi tiến độ)"},
            {"id": "mt_10", "cau_hoi": "Bạn có ăn mừng những thành tựu nhỏ trên con đường đạt mục tiêu lớn không?", "loai": "Quản lý mục tiêu (Ăn mừng thành tựu nhỏ)"},
        ],
        "muc_do_tu_nhan_thuc": [
            # Hiện có 4, thêm 6
            {"id": "tnt_1", "cau_hoi": "Bạn có nhận biết rõ ràng những điểm mạnh của bản thân không?", "loai": "Tự nhận thức (Điểm mạnh)"},
            {"id": "tnt_2", "cau_hoi": "Bạn có ý thức được những điểm yếu cần cải thiện của mình không?", "loai": "Tự nhận thức (Điểm yếu)"},
            {"id": "tnt_3", "cau_hoi": "Bạn có thường xuyên suy ngẫm về cảm xúc và hành vi của mình không?", "loai": "Tự nhận thức (Cảm xúc & Hành vi)"},
            {"id": "tnt_4", "cau_hoi": "Bạn có hiểu rõ những yếu tố nào thường ảnh hưởng đến quyết định của bạn không?", "loai": "Tự nhận thức (Yếu tố ảnh hưởng quyết định)"},
            {"id": "tnt_5", "cau_hoi": "Bạn có nhận biết được cảm xúc của người khác qua biểu hiện của họ không?", "loai": "Nhận thức xã hội (Đọc vị cảm xúc)"},
            {"id": "tnt_6", "cau_hoi": "Bạn có hiểu được hành động của mình ảnh hưởng đến người khác như thế nào không?", "loai": "Tự nhận thức (Ảnh hưởng đến người khác)"},
            {"id": "tnt_7", "cau_hoi": "Bạn có cởi mở đón nhận những phản hồi mang tính xây dựng về bản thân không?", "loai": "Tự nhận thức (Đón nhận phản hồi)"},
            {"id": "tnt_8", "cau_hoi": "Bạn có biết những tình huống nào dễ khiến bạn căng thẳng hoặc mất bình tĩnh không?", "loai": "Tự nhận thức (Tác nhân căng thẳng)"},
            {"id": "tnt_9", "cau_hoi": "Bạn có thể mô tả các giá trị quan trọng nhất đối với bạn một cách rõ ràng không?", "loai": "Tự nhận thức (Giá trị cá nhân)"},
            {"id": "tnt_10", "cau_hoi": "Bạn có nhận ra những 'điểm mù' (những điều người khác thấy ở bạn mà bạn không thấy) của mình không?", "loai": "Tự nhận thức (Điểm mù)"},
        ]
    }
    # Đếm tổng số câu hỏi
    tong_so_cau_hoi = sum(len(ds) for ds in cau_hoi.values())
    print(f"Tổng số câu hỏi được khởi tạo: {tong_so_cau_hoi}") # Debug
    return cau_hoi

# --- PHẦN 2: THỰC HIỆN ĐÁNH GIÁ ---
def thuc_hien_danh_gia(danh_sach_cau_hoi):
    """
    Hiển thị câu hỏi cho người dùng và thu thập câu trả lời.
    Người dùng nhập điểm từ 1 (Hoàn toàn không đồng ý) đến 5 (Hoàn toàn đồng ý).
    """
    print("\nChào mừng bạn đến với Hệ thống Tự đánh giá Cá nhân!")
    print("Vui lòng trả lời các câu hỏi sau theo thang điểm từ 1 đến 5:")
    print("1: Hoàn toàn không đồng ý / Rất kém")
    print("2: Không đồng ý / Kém")
    print("3: Trung lập / Trung bình")
    print("4: Đồng ý / Tốt")
    print("5: Hoàn toàn đồng ý / Rất tốt")
    print("-" * 50)

    ket_qua_tra_loi = []
    for danh_muc_chung, ds_cau_hoi_trong_muc in danh_sach_cau_hoi.items():
        print(f"\n--- {danh_muc_chung.replace('_', ' ').upper()} ---")
        for cau_hoi_info in ds_cau_hoi_trong_muc:
            while True:
                try:
                    tra_loi = input(f"{cau_hoi_info['cau_hoi']} (1-5): ")
                    diem = int(tra_loi)
                    if 1 <= diem <= 5:
                        ket_qua_tra_loi.append({
                            "id_cau_hoi": cau_hoi_info["id"],
                            "cau_hoi": cau_hoi_info["cau_hoi"],
                            "loai_cau_hoi": cau_hoi_info["loai"],
                            "danh_muc_chung": danh_muc_chung,
                            "diem_so": diem
                        })
                        break
                    else:
                        print("Vui lòng nhập một số từ 1 đến 5.")
                except ValueError:
                    print("Dữ liệu không hợp lệ. Vui lòng nhập một số.")
    return ket_qua_tra_loi

# --- PHẦN 3: LƯU TRỮ KẾT QUẢ ---
def luu_ket_qua(ket_qua_tra_loi, ten_nguoi_dung="nguoi_dung_mac_dinh", thu_muc_ket_qua="ket_qua_danh_gia"):
    """
    Lưu kết quả trả lời của người dùng vào file JSON.
    Tên file sẽ bao gồm tên người dùng và ngày giờ thực hiện.
    """
    if not os.path.exists(thu_muc_ket_qua):
        os.makedirs(thu_muc_ket_qua)
        print(f"Đã tạo thư mục: {thu_muc_ket_qua}")

    thoi_gian = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ten_file = f"{ten_nguoi_dung}_{thoi_gian}.json"
    duong_dan_file = os.path.join(thu_muc_ket_qua, ten_file)

    try:
        with open(duong_dan_file, 'w', encoding='utf-8') as f:
            json.dump(ket_qua_tra_loi, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu kết quả đánh giá vào: {duong_dan_file}")
        return duong_dan_file
    except IOError as e:
        print(f"Lỗi khi lưu file: {e}")
        return None

# --- PHẦN 4: ĐỌC KẾT QUẢ ---
def doc_ket_qua(duong_dan_file):
    """
    Đọc kết quả đánh giá từ file JSON.
    """
    try:
        with open(duong_dan_file, 'r', encoding='utf-8') as f:
            ket_qua_tra_loi = json.load(f)
        print(f"Đã đọc thành công kết quả từ: {duong_dan_file}")
        return ket_qua_tra_loi
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {duong_dan_file}")
        return None
    except json.JSONDecodeError:
        print(f"Lỗi: File {duong_dan_file} không phải là định dạng JSON hợp lệ.")
        return None
    except Exception as e:
        print(f"Lỗi không xác định khi đọc file: {e}")
        return None

def chon_file_ket_qua(thu_muc_ket_qua="ket_qua_danh_gia"):
    """
    Hiển thị danh sách các file kết quả và cho người dùng chọn.
    """
    if not os.path.exists(thu_muc_ket_qua) or not os.listdir(thu_muc_ket_qua):
        print(f"Không tìm thấy file kết quả nào trong thư mục '{thu_muc_ket_qua}'.")
        return None

    files = [f for f in os.listdir(thu_muc_ket_qua) if f.endswith('.json')]
    if not files:
        print(f"Không tìm thấy file .json nào trong thư mục '{thu_muc_ket_qua}'.")
        return None

    print("\nCác file kết quả hiện có:")
    for i, ten_file in enumerate(files):
        print(f"{i + 1}. {ten_file}")

    while True:
        try:
            lua_chon = int(input("Chọn số thứ tự của file để phân tích: "))
            if 1 <= lua_chon <= len(files):
                return os.path.join(thu_muc_ket_qua, files[lua_chon - 1])
            else:
                print(f"Vui lòng chọn một số từ 1 đến {len(files)}.")
        except ValueError:
            print("Lựa chọn không hợp lệ. Vui lòng nhập số.")


# --- PHẦN 5: PHÂN TÍCH KẾT QUẢ ---
def phan_tich_ket_qua(ket_qua_tra_loi):
    """
    Phân tích kết quả trả lời, tính điểm trung bình cho từng loại và danh mục.
    Trả về một Pandas DataFrame chứa kết quả phân tích.
    """
    if not ket_qua_tra_loi:
        print("Không có dữ liệu để phân tích.")
        return None, None

    df = pd.DataFrame(ket_qua_tra_loi)

    # Tính điểm trung bình cho từng 'loai_cau_hoi' (chi tiết)
    diem_tb_theo_loai = df.groupby('loai_cau_hoi')['diem_so'].mean().sort_values(ascending=False)
    print("\n--- ĐIỂM TRUNG BÌNH THEO LOẠI CHI TIẾT ---")
    print(diem_tb_theo_loai)

    # Tính điểm trung bình cho từng 'danh_muc_chung' (tổng quát)
    diem_tb_theo_danh_muc = df.groupby('danh_muc_chung')['diem_so'].mean().sort_values(ascending=False)
    print("\n--- ĐIỂM TRUNG BÌNH THEO DANH MỤC CHUNG ---")
    print(diem_tb_theo_danh_muc)

    # Xác định điểm mạnh/yếu dựa trên điểm trung bình chung của danh mục
    # (Có thể điều chỉnh ngưỡng này)
    nguong_diem_manh = 4.0
    nguong_diem_yeu = 2.5 # Có thể là 3.0 tùy theo quan điểm

    diem_manh = diem_tb_theo_danh_muc[diem_tb_theo_danh_muc >= nguong_diem_manh]
    diem_yeu = diem_tb_theo_danh_muc[diem_tb_theo_danh_muc <= nguong_diem_yeu]

    print("\n--- ĐIỂM MẠNH NỔI BẬT (Danh mục chung) ---")
    if not diem_manh.empty:
        print(diem_manh)
    else:
        print("Không có điểm mạnh nổi bật rõ rệt (trung bình >= 4.0).")

    print("\n--- KHÍA CẠNH CẦN CẢI THIỆN (Danh mục chung) ---")
    if not diem_yeu.empty:
        print(diem_yeu)
    else:
        print("Không có khía cạnh nào cần cải thiện rõ rệt (trung bình <= 2.5).")
        
    # Đối chiếu dữ liệu (ví dụ: Trí thông minh vs Động lực)
    # Đây là một ví dụ đơn giản, có thể mở rộng với các kỹ thuật phức tạp hơn
    try:
        diem_tb_tri_thong_minh = df[df['danh_muc_chung'] == 'tri_thong_minh_noi_troi']['diem_so'].mean()
        diem_tb_dong_luc = df[df['danh_muc_chung'] == 'dong_luc_hoc_tap_hanh_dong']['diem_so'].mean()
        print("\n--- ĐỐI CHIẾU SƠ BỘ ---")
        print(f"Điểm trung bình Trí thông minh nổi trội: {diem_tb_tri_thong_minh:.2f}")
        print(f"Điểm trung bình Động lực học tập & hành động: {diem_tb_dong_luc:.2f}")
    except Exception as e:
        print(f"Không thể thực hiện đối chiếu do thiếu dữ liệu hoặc lỗi: {e}")


    return diem_tb_theo_loai, diem_tb_theo_danh_muc

# --- PHẦN 6: TRỰC QUAN HÓA KẾT QUẢ ---
def ve_bieu_do_radar_nang_luc(diem_tb_theo_danh_muc, ten_nguoi_dung="nguoi_dung", thu_muc_bieu_do="bieu_do_danh_gia"):
    """
    Vẽ biểu đồ radar cho các danh mục năng lực chính.
    """
    if diem_tb_theo_danh_muc is None or diem_tb_theo_danh_muc.empty:
        print("Không có dữ liệu điểm trung bình theo danh mục để vẽ biểu đồ radar.")
        return

    labels = diem_tb_theo_danh_muc.index.to_list()
    stats = diem_tb_theo_danh_muc.values.flatten().tolist()
    
    num_vars = len(labels)

    # Tính toán góc cho mỗi trục
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    stats += stats[:1] # Đóng vòng radar
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, stats, linewidth=2, linestyle='solid', color='skyblue', label="Điểm trung bình")
    ax.fill(angles, stats, 'skyblue', alpha=0.4)

    # Đặt nhãn cho các trục
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    # Đặt giới hạn trục y (thang điểm 1-5)
    ax.set_yticks(np.arange(1, 6, 1))
    ax.set_yticklabels([str(i) for i in range(1, 6)], fontsize=9)
    ax.set_ylim(0, 5) # Thang điểm từ 0 đến 5

    plt.title(f'Bản đồ Năng lực Cá nhân - {ten_nguoi_dung}', size=16, y=1.1, fontdict={'fontsize': 15, 'fontweight': 'bold'})
    ax.grid(True)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Lưu biểu đồ
    if not os.path.exists(thu_muc_bieu_do):
        os.makedirs(thu_muc_bieu_do)
    ten_file_bieu_do = f"radar_{ten_nguoi_dung}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    duong_dan_file_bieu_do = os.path.join(thu_muc_bieu_do, ten_file_bieu_do)
    try:
        plt.savefig(duong_dan_file_bieu_do, bbox_inches='tight')
        print(f"Đã lưu biểu đồ Radar vào: {duong_dan_file_bieu_do}")
    except Exception as e:
        print(f"Lỗi khi lưu biểu đồ Radar: {e}")
    plt.show()


def ve_bieu_do_cot_so_sanh(diem_tb_theo_loai, ten_nhom_cau_hoi, ten_nguoi_dung="nguoi_dung", thu_muc_bieu_do="bieu_do_danh_gia"):
    """
    Vẽ biểu đồ cột so sánh điểm số cho một nhóm câu hỏi cụ thể (ví dụ: các loại trí thông minh).
    `diem_tb_theo_loai` là Series pandas chứa điểm trung bình của tất cả các loại câu hỏi.
    `ten_nhom_cau_hoi` là một list các 'loai_cau_hoi' thuộc cùng một nhóm để vẽ.
    """
    if diem_tb_theo_loai is None or diem_tb_theo_loai.empty:
        print(f"Không có dữ liệu điểm trung bình theo loại để vẽ biểu đồ cột cho '{ten_nhom_cau_hoi}'.")
        return

    # Lọc ra các loại câu hỏi thuộc nhóm cần vẽ
    du_lieu_ve = diem_tb_theo_loai[diem_tb_theo_loai.index.isin(ten_nhom_cau_hoi)]

    if du_lieu_ve.empty:
        print(f"Không tìm thấy dữ liệu cho các loại câu hỏi trong nhóm '{ten_nhom_cau_hoi}'.")
        return

    plt.figure(figsize=(12, 7))
    bars = plt.bar(du_lieu_ve.index, du_lieu_ve.values, color=plt.cm.Paired(np.arange(len(du_lieu_ve))))
    plt.ylabel('Điểm Trung Bình (1-5)', fontsize=12)
    plt.xlabel('Loại hình', fontsize=12)
    
    # Lấy tên danh mục chung từ một trong các loại câu hỏi (giả định chúng cùng danh mục)
    # Điều này có thể cần cải tiến nếu các 'loai_cau_hoi' từ các 'danh_muc_chung' khác nhau
    title_group_name = ten_nhom_cau_hoi[0].split('(')[0].strip() if ten_nhom_cau_hoi else "So sánh điểm"
    
    plt.title(f'So sánh Điểm: {title_group_name} - {ten_nguoi_dung}', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(np.arange(0, 5.5, 0.5), fontsize=10)
    plt.ylim(0, 5.5) # Mở rộng trục y một chút
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout() # Điều chỉnh layout cho vừa vặn

    # Thêm giá trị trên mỗi cột
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05, f'{yval:.2f}', ha='center', va='bottom', fontsize=9)

    # Lưu biểu đồ
    if not os.path.exists(thu_muc_bieu_do):
        os.makedirs(thu_muc_bieu_do)
    
    # Tạo tên file an toàn hơn
    safe_title_group_name = "".join(c if c.isalnum() else "_" for c in title_group_name)
    ten_file_bieu_do = f"bar_{safe_title_group_name}_{ten_nguoi_dung}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    duong_dan_file_bieu_do = os.path.join(thu_muc_bieu_do, ten_file_bieu_do)
    try:
        plt.savefig(duong_dan_file_bieu_do, bbox_inches='tight')
        print(f"Đã lưu biểu đồ Cột vào: {duong_dan_file_bieu_do}")
    except Exception as e:
        print(f"Lỗi khi lưu biểu đồ Cột: {e}")
    plt.show()


def ve_bieu_do_tron_ty_le(diem_tb_theo_loai, ten_nhom_cau_hoi, ten_nguoi_dung="nguoi_dung", thu_muc_bieu_do="bieu_do_danh_gia"):
    """
    Vẽ biểu đồ tròn thể hiện tỷ lệ điểm số cho một nhóm câu hỏi.
    Hữu ích cho việc xem xét tỷ trọng các giá trị hoặc xu hướng động lực.
    `diem_tb_theo_loai` là Series pandas.
    `ten_nhom_cau_hoi` là list các 'loai_cau_hoi' thuộc nhóm đó.
    """
    if diem_tb_theo_loai is None or diem_tb_theo_loai.empty:
        print(f"Không có dữ liệu điểm trung bình theo loại để vẽ biểu đồ tròn cho '{ten_nhom_cau_hoi}'.")
        return

    du_lieu_ve = diem_tb_theo_loai[diem_tb_theo_loai.index.isin(ten_nhom_cau_hoi)]

    if du_lieu_ve.empty or du_lieu_ve.sum() == 0: # Kiểm tra tổng khác 0
        print(f"Không tìm thấy dữ liệu hoặc tổng điểm bằng 0 cho nhóm '{ten_nhom_cau_hoi}'. Không thể vẽ biểu đồ tròn.")
        return

    labels = du_lieu_ve.index
    sizes = du_lieu_ve.values
    
    # Lấy tên danh mục chung từ một trong các loại câu hỏi
    title_group_name = ten_nhom_cau_hoi[0].split('(')[0].strip() if ten_nhom_cau_hoi else "Tỷ lệ"

    plt.figure(figsize=(10, 8))
    # explode = (0.1, 0, 0, 0)  # chỉ "explode" lát đầu tiên (nếu muốn)
    # colors = plt.cm.Pastel1(np.arange(len(sizes))/len(sizes)) # Bảng màu pastel
    wedges, texts, autotexts = plt.pie(sizes, autopct='%1.1f%%', startangle=140,
                                       textprops=dict(color="w")) # Màu chữ phần trăm là trắng

    plt.legend(wedges, labels, title="Chú giải", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
    plt.setp(autotexts, size=10, weight="bold") # Chỉnh kích thước, độ đậm chữ phần trăm
    plt.title(f'Tỷ lệ {title_group_name} - {ten_nguoi_dung}', fontsize=16, fontweight='bold')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()

    # Lưu biểu đồ
    if not os.path.exists(thu_muc_bieu_do):
        os.makedirs(thu_muc_bieu_do)
    safe_title_group_name = "".join(c if c.isalnum() else "_" for c in title_group_name)
    ten_file_bieu_do = f"pie_{safe_title_group_name}_{ten_nguoi_dung}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    duong_dan_file_bieu_do = os.path.join(thu_muc_bieu_do, ten_file_bieu_do)
    try:
        plt.savefig(duong_dan_file_bieu_do, bbox_inches='tight')
        print(f"Đã lưu biểu đồ Tròn vào: {duong_dan_file_bieu_do}")
    except Exception as e:
        print(f"Lỗi khi lưu biểu đồ Tròn: {e}")
    plt.show()

# --- PHẦN 7: XUẤT BÁO CÁO (Placeholder) ---
def xuat_bao_cao(ten_nguoi_dung, diem_tb_theo_loai, diem_tb_theo_danh_muc, thu_muc_bieu_do="bieu_do_danh_gia"):
    """
    Hàm này hiện tại chỉ lưu các biểu đồ dưới dạng file ảnh.
    Có thể mở rộng để tạo file PDF/HTML báo cáo hoàn chỉnh.
    """
    print("\n--- XUẤT BÁO CÁO ---")
    print("Các biểu đồ đã được lưu dưới dạng file PNG trong thư mục:", thu_muc_bieu_do)
    
    # Gọi các hàm vẽ biểu đồ để đảm bảo chúng được tạo và lưu nếu chưa
    # (Trong luồng chính, chúng thường đã được gọi rồi)
    
    # Ví dụ: Vẽ và lưu radar chart (nếu chưa có)
    if diem_tb_theo_danh_muc is not None and not diem_tb_theo_danh_muc.empty:
        ve_bieu_do_radar_nang_luc(diem_tb_theo_danh_muc, ten_nguoi_dung, thu_muc_bieu_do)
    
    # Ví dụ: Vẽ và lưu bar chart cho Trí thông minh
    cau_hoi_goc = khoi_tao_cau_hoi() # Lấy lại cấu trúc câu hỏi để lấy tên nhóm
    nhom_tri_thong_minh = [q['loai'] for q in cau_hoi_goc['tri_thong_minh_noi_troi']]
    if diem_tb_theo_loai is not None and not diem_tb_theo_loai.empty:
         ve_bieu_do_cot_so_sanh(diem_tb_theo_loai, nhom_tri_thong_minh, ten_nguoi_dung, thu_muc_bieu_do)

    # Ví dụ: Vẽ và lưu pie chart cho Giá trị cốt lõi
    nhom_gia_tri_cot_loi = [q['loai'] for q in cau_hoi_goc['gia_tri_cot_loi']]
    if diem_tb_theo_loai is not None and not diem_tb_theo_loai.empty:
        ve_bieu_do_tron_ty_le(diem_tb_theo_loai, nhom_gia_tri_cot_loi, ten_nguoi_dung, thu_muc_bieu_do)
    
    print("Để tạo báo cáo PDF/HTML hoàn chỉnh, cần tích hợp thêm các thư viện như ReportLab, WeasyPrint hoặc FPDF.")


# --- PHẦN 8: HÀM MAIN ĐIỀU KHIỂN ---
def main():
    """
    Hàm chính điều khiển luồng của ứng dụng.
    """
    cau_hoi_danh_gia = khoi_tao_cau_hoi()
    ten_nguoi_dung = "" # Sẽ lấy từ input
    duong_dan_file_ket_qua_moi_nhat = None

    while True:
        print("\n--- HỆ THỐNG TỰ ĐÁNH GIÁ CÁ NHÂN ---")
        print("1. Thực hiện bài đánh giá mới")
        print("2. Phân tích kết quả đã lưu")
        print("3. Thoát")
        lua_chon_chinh = input("Nhập lựa chọn của bạn (1-3): ")

        if lua_chon_chinh == '1':
            if not ten_nguoi_dung: # Chỉ hỏi tên lần đầu hoặc nếu chưa có
                 while True:
                    ten_nguoi_dung_tam = input("Nhập tên của bạn (để lưu file kết quả, ví dụ: 'NguyenVanA'): ").strip()
                    if ten_nguoi_dung_tam: # Kiểm tra xem người dùng có nhập gì không
                        # Loại bỏ các ký tự không hợp lệ cho tên file
                        ten_nguoi_dung = "".join(c if c.isalnum() or c in ['_','-'] else '' for c in ten_nguoi_dung_tam)
                        if ten_nguoi_dung: # Kiểm tra lại sau khi làm sạch
                            break
                        else:
                            print("Tên không hợp lệ sau khi loại bỏ ký tự đặc biệt. Vui lòng thử lại.")
                    else:
                        print("Tên không được để trống. Vui lòng nhập tên.")


            ket_qua = thuc_hien_danh_gia(cau_hoi_danh_gia)
            duong_dan_file_ket_qua_moi_nhat = luu_ket_qua(ket_qua, ten_nguoi_dung)
            if duong_dan_file_ket_qua_moi_nhat:
                diem_tb_loai, diem_tb_danh_muc = phan_tich_ket_qua(ket_qua)
                if diem_tb_loai is not None and diem_tb_danh_muc is not None:
                    xuat_bao_cao(ten_nguoi_dung, diem_tb_loai, diem_tb_danh_muc) # Sẽ gọi các hàm vẽ bên trong

        elif lua_chon_chinh == '2':
            duong_dan_file_can_phan_tich = chon_file_ket_qua()
            if duong_dan_file_can_phan_tich:
                # Trích xuất tên người dùng từ tên file để hiển thị trên biểu đồ
                ten_file_chon = os.path.basename(duong_dan_file_can_phan_tich)
                # Giả định tên file có dạng TenNguoiDung_YYYYMMDD_HHMMSS.json
                ten_nguoi_dung_tu_file = ten_file_chon.split('_')[0]

                ket_qua_cu = doc_ket_qua(duong_dan_file_can_phan_tich)
                if ket_qua_cu:
                    diem_tb_loai, diem_tb_danh_muc = phan_tich_ket_qua(ket_qua_cu)
                    if diem_tb_loai is not None and diem_tb_danh_muc is not None:
                         xuat_bao_cao(ten_nguoi_dung_tu_file, diem_tb_loai, diem_tb_danh_muc)

        elif lua_chon_chinh == '3':
            print("Cảm ơn bạn đã sử dụng hệ thống. Hẹn gặp lại!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    main()
