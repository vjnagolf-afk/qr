# -*- coding: utf-8 -*-
import streamlit as st
import io
import os

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

# ============================================================
# CẤU HÌNH TRANG CHUẨN DASHBOARD (RỘNG & CHUYÊN NGHIỆP)
# ============================================================
st.set_page_config(
    page_title="Trợ lý Giáo viên - THCS Nguyễn Chí Thanh",
    page_icon="🎓",
    layout="wide",  # Đã chuyển thành giao diện rộng (wide)
    initial_sidebar_state="expanded"
)

# Nâng cấp CSS chuyên nghiệp hơn
st.markdown("""
    <style>
    /* Gradient Header */
    .main-header {
        background: linear-gradient(135deg, #0f4c81 0%, #162447 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .main-header p {
        margin: 10px 0 0 0;
        font-size: 16px;
        color: #e0e0e0;
        font-weight: 500;
    }
    
    /* Nút bấm tải xuống / xử lý */
    .stButton>button {
        width: 100%;
        background-color: #0f4c81;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1b6ca8;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Định dạng tabs để dễ nhìn hơn trên màn hình rộng */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8f0fe;
        border-bottom: 3px solid #0f4c81;
        color: #0f4c81;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR MENU)
# ============================================================
st.sidebar.markdown("### 📌 BẢNG ĐIỀU KHIỂN")
chuc_nang = st.sidebar.radio(
    "Chọn tính năng sử dụng:",
    ["📱 Tạo Mã QR Tùy Biến", "🤖 Chuyên gia Sinh Prompt AI"]
)
st.sidebar.divider()
st.sidebar.markdown(
    "<p style='text-align: center; color: gray; font-size: 13px;'>Tác giả: Lê Hồng Dưỡng<br>Trường THCS Nguyễn Chí Thanh 🏫</p>",
    unsafe_allow_html=True
)

# ============================================================
# TÍNH NĂNG 1: TẠO MÃ QR TÙY BIẾN
# ============================================================
if chuc_nang == "📱 Tạo Mã QR Tùy Biến":
    st.markdown("""
        <div class="main-header">
            <h1>🎓 TRƯỜNG THCS NGUYỄN CHÍ THANH</h1>
            <p>⚡ Trợ lý Tạo Mã QR Sạch, Không Quảng Cáo & Tùy Biến Chuyên Nghiệp</p>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2.5]) # Chia cột để giao diện rộng trông cân đối

    with col_left:
        with st.container(border=True):
            st.markdown("### 🎨 Tùy chỉnh phong cách")
            qr_color = st.color_picker("Chọn màu cho mã QR:", "#162447")
            bg_color = st.color_picker("Chọn màu nền QR:", "#ffffff")
            box_size_val = st.slider("Độ phân giải mã QR:", min_value=6, max_value=20, value=12)
            
            st.markdown("---")
            st.markdown("### ✍️ Tùy chỉnh văn bản")
            custom_font_size = st.slider("Cỡ chữ tên tác giả (Pixel):", min_value=14, max_value=100, value=36)
            banner_height_val = st.slider("Chiều cao khung chữ:", min_value=40, max_value=160, value=80)

    with col_right:
        with st.container(border=True):
            st.markdown("### 📥 Dữ liệu mã QR")
            target_link = st.text_input(
                "Link liên kết (Bắt buộc):",
                placeholder="VD: https://thcsnguyenchithanh-lhd.streamlit.app/..."
            )

            creator_name = st.text_input(
                "Tên hiển thị dưới mã QR (Tùy chọn):",
                placeholder="VD: Thầy Lê Hồng Dưỡng"
            )

            if target_link:
                if HAS_QRCODE:
                    try:
                        qr = qrcode.QRCode(
                            version=2,
                            error_correction=qrcode.constants.ERROR_CORRECT_H,
                            box_size=box_size_val,
                            border=4
                        )
                        qr.add_data(target_link)
                        qr.make(fit=True)
                        
                        img_qr = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')
                        
                        if creator_name.strip():
                            qr_width, qr_height = img_qr.size

                            new_img = Image.new("RGB", (qr_width, qr_height + banner_height_val), color=bg_color)
                            new_img.paste(img_qr, (0, 0))
                            
                            draw = ImageDraw.Draw(new_img)
                            
                            font_paths = [
                                "timesbd.ttf",  # Times New Roman Bold (In đậm)
                                "times.ttf",    # Times New Roman Thường
                                "DejaVuSans-Bold.ttf",
                                "DejaVuSans.ttf"
                            ]
                            
                            font = None
                            for path in font_paths:
                                try:
                                    font = ImageFont.truetype(path, custom_font_size)
                                    break
                                except:
                                    continue
                            
                            if font is None:
                                font = ImageFont.load_default()
                            
                            text_to_display = f"Người tạo: {creator_name.strip()}"
                            
                            draw.rectangle([(0, qr_height), (qr_width, qr_height + banner_height_val)], fill=qr_color)
                            
                            bbox = draw.textbbox((0, 0), text_to_display, font=font)
                            text_w = bbox[2] - bbox[0]
                            text_h = bbox[3] - bbox[1]
                            
                            text_x = (qr_width - text_w) / 2
                            text_y = qr_height + (banner_height_val - text_h) / 2
                            
                            draw.text((text_x, text_y), text_to_display, fill="#ffffff", font=font)
                            final_img = new_img
                        else:
                            final_img = img_qr

                        buf = io.BytesIO()
                        final_img.save(buf, format="PNG")
                        
                        st.markdown("---")
                        st.markdown("#### 📱 KẾT QUẢ MÃ QR")
                        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
                        with col_img2:
                            st.image(buf.getvalue(), caption="Quét mã để truy cập trực tiếp", use_container_width=True)
                            
                            st.download_button(
                                label="📥 TẢI ẢNH MÃ QR HOÀN CHỈNH (.PNG)",
                                data=buf.getvalue(),
                                file_name="ma_qr_truong_thcs_nguyen_chi_thanh.png",
                                mime="image/png",
                                type="primary"
                            )
                    except Exception as e:
                        st.error(f"⚠️ Có lỗi xảy ra trong quá trình tạo: {e}")
                else:
                    st.error("⚠️ Máy chủ chưa cài đặt thư viện qrcode.")
            else:
                st.info("💡 Điền đường link vào ô bên trên để hệ thống tạo mã QR.")

# ============================================================
# TÍNH NĂNG 2: CHUYÊN GIA SINH PROMPT AI
# ============================================================
elif chuc_nang == "🤖 Chuyên gia Sinh Prompt AI":
    st.markdown("""
        <div class="main-header">
            <h1>🤖 CHUYÊN GIA SINH PROMPT SƯ PHẠM</h1>
            <p>⚡ Thư viện câu lệnh (Prompt) chuẩn hóa tối ưu hóa sức mạnh AI trong giáo dục</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("⚠️ QUY TẮC VÀ LƯU Ý QUAN TRỌNG KHI SỬ DỤNG AI", expanded=True):
        st.markdown("""
        1. **Xác thực thông tin (Fact-checking):** AI có thể tạo ra thông tin không chính xác. Thầy cô bắt buộc phải kiểm duyệt chuyên môn kỹ lưỡng trước khi đưa vào bài giảng.
        2. **Bảo mật dữ liệu:** Không đưa thông tin cá nhân, điểm số học sinh hoặc văn bản nội bộ mật của trường lên AI công cộng.
        3. **Giữ vững vai trò chủ đạo:** AI chỉ là trợ lý. Tư duy sư phạm và sự thấu hiểu học sinh của người thầy là không thể thay thế.
        4. **Hướng dẫn học sinh trung thực:** Dạy các em dùng AI để gợi mở ý tưởng, phản biện, tuyệt đối không lạm dụng copy/paste để đối phó bài tập.
        """)
    st.markdown("<br>", unsafe_allow_html=True)

    tab_khbd, tab_khao_thi, tab_tinh_huong, tab_hs, tab_ta = st.tabs([
        "📚 1. Kế hoạch bài dạy & Slide", 
        "📝 2. Khảo thí & Đề kiểm tra", 
        "🧩 3. Tình huống & Thảo luận", 
        "🎓 4. Trợ lý Học sinh", 
        "🇬🇧 5. Chuyên biệt Tiếng Anh"
    ])

    with tab_khbd:
        st.markdown("#### 📚 Prompt Soạn Kế hoạch bài dạy & Thiết kế Slide")
        loai_khbd = st.radio("Chọn biểu mẫu Prompt:", [
            "KHBD Chuẩn CV 5512 & GDPT 2018 (Chi tiết, toàn diện)", 
            "KHBD Tích hợp Năng lực số (Dành cho Eduaide/MagicSchool)", 
            "Thẩm định Kế hoạch bài dạy (Góc độ Tổ trưởng chuyên môn)",
            "Thiết kế Slide bài giảng (Dùng cho AI Gamma.app, Canva Magic Design)"
        ], horizontal=True)

        if "Chuẩn CV 5512" in loai_khbd:
            st.info("💡 **Mục đích:** Xây dựng giáo án chi tiết 4 hoạt động, có tích hợp STEM, AI và phương án phân hóa học sinh.")
            prompt_khbd_chuan = """# 1. VAI TRÒ
Bạn là Chuyên gia Giáo dục cấp cao của Việt Nam, có nhiều năm kinh nghiệm biên soạn Kế hoạch bài dạy (KHBD) theo Chương trình Giáo dục phổ thông 2018.
Bạn am hiểu sâu về Công văn 5512/BGDĐT, Yêu cầu cần đạt, Giáo dục STEM, Khung năng lực số (Thông tư 02/2024/BGDĐT) và các phương pháp dạy học tích cực.

# 2. THÔNG TIN ĐẦU VÀO
* Môn học: [Nhập môn học]
* Lớp: [Nhập khối lớp]
* Bộ sách: [Nhập tên bộ sách]
* Bài học: [Nhập tên bài]
* Thời lượng: [Số tiết]
* Yêu cầu cần đạt: [Dán YCCĐ vào đây]

# 3. YÊU CẦU CẤU TRÚC (BẮT BUỘC DẠNG BẢNG)
I. Thông tin chung
II. Mục tiêu (Kiến thức, Năng lực đặc thù, Năng lực chung, Phẩm chất đo lường được).
III. Thiết bị dạy học và học liệu.
IV. Tiến trình dạy học (Gồm 4 HĐ: Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng).
Mỗi hoạt động BẮT BUỘC trình bày 4 bước: (1) Chuyển giao nhiệm vụ, (2) Thực hiện nhiệm vụ, (3) Báo cáo thảo luận, (4) Kết luận nhận định.
Viết rõ lời nói của giáo viên và hành động của học sinh.

# 4. TÍCH HỢP BẮT BUỘC
- Cuối mỗi hoạt động có mục: Tích hợp AI (Gợi ý công cụ, Prompt mẫu, vai trò).
- Đánh giá năng lực số học sinh theo TT 02/2024 (Khai thác TT, Giao tiếp, Hợp tác...).
- Giáo dục STEM (nếu phù hợp).
- Phân hóa học sinh (Chậm, trung bình, khá giỏi).
- Các Phụ lục (Bảng tổng hợp AI, Học liệu số, Rubric, Câu hỏi đánh giá, Bài tập về nhà)."""
            st.code(prompt_khbd_chuan, language="markdown")
            
        elif "Năng lực số" in loai_khbd:
            st.info("💡 **Mục đích:** Soạn giáo án tập trung vào việc hình thành 6 tiêu chuẩn năng lực số của học sinh.")
            prompt_magicschool = """Hãy soạn giáo án hoàn toàn bằng tiếng Việt và bắt buộc phải tuân theo cấu trúc chuẩn của Công văn 5512/BGDĐT-GDTrH bao gồm đầy đủ các phần sau:
I. MỤC TIÊU: 
1. Về kiến thức; 
2. Về năng lực; (Phải có đầy đủ 3 nhóm năng lực: a) Năng lực chung; b) Năng lực đặc thù; c) Năng lực số và AI). 
(Phần Năng lực số và AI phải thực hiện đúng các mảng năng lực số và các chỉ báo mức độ theo Thông tư 02/2025 của Bộ Giáo dục và Đào tạo)
3. Về phẩm chất.

II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU.
III. TIẾN TRÌNH DẠY HỌC: 
Thiết kế đủ 4 hoạt động học tập (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng). Mỗi hoạt động chia rõ 4 mục: a) Mục tiêu; b) Nội dung; c) Sản phẩm; d) Tổ chức thực hiện (Chuyển giao, Thực hiện, Báo cáo, Kết luận).

# TÍCH HỢP NĂNG LỰC SỐ
Mỗi hoạt động cần chỉ rõ học sinh được hình thành:
- Khai thác thông tin số
- Giao tiếp số
- Hợp tác số
- Sáng tạo nội dung số
- An toàn số
- Giải quyết vấn đề bằng công nghệ số
Đánh dấu mức độ (Có/Không) và mô tả hành động cụ thể của học sinh."""
            st.code(prompt_magicschool, language="markdown")

        elif "Thiết kế Slide" in loai_khbd:
            st.info("💡 **Cách dùng:** Điền thông tin vào khoảng trống `[...]`, copy toàn bộ dán vào ChatGPT/Gemini. Lấy kịch bản thu được dán vào nền tảng Gamma.app để AI tự động vẽ slide.")
            prompt_slide = """# VAI TRÒ
Bạn là chuyên gia thiết kế bài giảng điện tử (E-learning), chuyên gia Presentation Design (PowerPoint, Canva, Gamma) và là giáo viên dày dặn kinh nghiệm giảng dạy theo Chương trình GDPT 2018 của Việt Nam. Khả năng đặc biệt của bạn là chuyển hóa kiến thức học thuật thành nội dung trực quan, tối giản, dễ hiểu và hấp dẫn học sinh THCS.

# THÔNG TIN ĐẦU VÀO
- Môn học: [Điền môn học]
- Lớp: [Điền lớp]
- Tên bài học: [Điền tên bài]
- Thời lượng: [Điền thời lượng, ví dụ: 45 phút]
- Mục tiêu bài học: [Điền mục tiêu]
- Nội dung tóm tắt/SGK: [Copy/paste nội dung SGK hoặc tóm tắt vào đây]

# MỤC TIÊU & QUY TẮC THIẾT KẾ (RẤT QUAN TRỌNG)
Tạo kịch bản slide bài giảng hoàn chỉnh tuân thủ TUYỆT ĐỐI các quy tắc sau:

1. Nguyên tắc Đa phương tiện (Multimedia Learning - Richard Mayer):
   - Coherence: Loại bỏ hoàn toàn thông tin, hình ảnh, từ ngữ thừa.
   - Signaling: Dùng các dấu hiệu (in đậm, màu sắc) để làm nổi bật ý chính.
   - Redundancy: Không lặp lại nguyên văn chữ trên slide vào lời giảng.
   - Spatial Contiguity: Sắp xếp chữ phải đặt sát ngay cạnh hình ảnh liên quan.
   - Temporal Contiguity: Lời giảng và hình ảnh/hiệu ứng phải xuất hiện đồng thời.
   - Segmenting: Chia nhỏ nội dung phức tạp thành các slide/bước nhỏ dễ tiêu hóa.
   - Personalization: Sử dụng ngôn ngữ xưng hô gần gũi, phù hợp học sinh THCS.

2. Phong cách & Màu sắc:
   - Thiết kế Tối giản (Minimalism), nhiều khoảng trắng, font Sans Serif dễ đọc.
   - Tối đa 3 màu: 1 màu chính, 1 màu nhấn, 1 màu trung tính. Tuyệt đối không dùng quá nhiều màu lòe loẹt.

3. Giới hạn Text (Quy tắc thép):
   - 1 Slide = 1 Thông điệp.
   - Tiêu đề: Ngắn gọn, nổi bật, TỐI ĐA 10 TỪ.
   - Nội dung chữ: Dạng bullet point. TỐI ĐA 3-5 ý/slide. TỐI ĐA 12 từ/ý. KHÔNG viết đoạn văn.

4. Trực quan hóa (Visual First): 
   - BẮT BUỘC: Mỗi slide phải có ít nhất một thành phần trực quan (icon, infographic, sơ đồ, timeline, bảng, hình minh họa, ảnh thực tế, mô hình 3D, biểu đồ).
   - Không được phép tạo slide toàn chữ.

5. Hiệu ứng (Animation/Transition):
   - Chỉ sử dụng các hiệu ứng chuyên nghiệp: Fade, Appear, Wipe, hoặc Morph.
   - Tuyệt đối KHÔNG đề xuất các hiệu ứng gây rối mắt (Bounce, Fly, Spin...).

6. Tương tác & Đánh giá: 
   - Lồng ghép linh hoạt (Câu hỏi, Mini game, Thí nghiệm, QR Code, Video...).
   - Xác định rõ mức độ nhận thức theo Thang Bloom cho từng slide.

# ĐẦU RA YÊU CẦU
Hãy thiết kế lần lượt TOÀN BỘ bài học, không rút gọn, không bỏ sót phần nào. Nếu quá dài, hãy dừng lại ở slide hợp lý và đợi tôi gõ "Tiếp tục". 

Trình bày MỖI SLIDE theo đúng định dạng Template dưới đây:

---
### Slide [Số thứ tự]: [Tên Slide - Tối đa 10 từ]
- **Mục tiêu Slide:** [1 câu ngắn gọn]
- **Mức tư duy Bloom:** [Remember / Understand / Apply / Analyze / Evaluate / Create]
- **Bố cục thiết kế:** [Đề xuất: Left text + Right image / 3 columns / Mindmap / Timeline / Table / Full image...]
- **Nội dung trên Slide (Text hiển thị):**
  + Ý 1: [Tối đa 12 từ]
  + Ý 2: [Tối đa 12 từ]
  + Ý 3: [Tối đa 12 từ]
- **Thành phần Trực quan & Hình ảnh:**
  + Mô tả: [Ghi rõ loại thành phần (VD: Sơ đồ, Icon, Ảnh thực tế) và mô tả chi tiết]
  + Prompt tạo ảnh AI: "[Viết 1 prompt tiếng Anh chi tiết. VD: A realistic illustration of...]"
- **Hiệu ứng & Tương tác (Nếu có):** [Chỉ định Fade/Appear/Wipe/Morph và Hoạt động tương tác]
- **Ghi chú cho Giáo viên (Speaker Notes):**
  + Gợi ý lời giảng: [2-4 câu diễn giải tự nhiên, cuốn hút, không đọc lại chữ trên slide]
  + Thời lượng dự kiến: [X phút]
---"""
            st.code(prompt_slide, language="markdown")
            
        else:
            st.info("💡 **Mục đích:** Kiểm tra và chỉ ra các điểm phi logic, thiếu sót trong giáo án.")
            prompt_thamdinh = """Đóng vai là một Tổ trưởng chuyên môn cấp THCS có chuyên môn sâu về sư phạm, công nghệ thông tin và ứng dụng AI trong giáo dục. 
Nhiệm vụ của bạn là đọc, phân tích và thẩm định Kế hoạch bài dạy (KHBD) dưới đây dựa trên 5 tiêu chí:
1. Sư phạm (Theo CV 5512).
2. Ứng dụng CNTT.
3. Tích hợp Năng lực số (Theo TT 02/2025).
4. Năng lực AI.
5. Kiểm tra, Đánh giá.

# YÊU CẦU ĐẦU RA:
Trình bày kết quả dưới dạng "PHIẾU THẨM ĐỊNH KẾ HOẠCH BÀI DẠY":
I. NHẬN XÉT TỔNG QUAN (2 điểm sáng, 1 lỗ hổng lớn nhất).
II. PHÂN TÍCH 5 TIÊU CHÍ (Chấm thang Đạt/Cần cải thiện/Xuất sắc. BẮT BUỘC trích dẫn minh chứng từ giáo án).
III. YÊU CẦU ĐIỀU CHỈNH (3 gợi ý chỉnh sửa trực tiếp, thực tế).

Nội dung giáo án cần thẩm định:
[DÁN GIÁO ÁN CỦA BẠN VÀO ĐÂY]"""
            st.code(prompt_thamdinh, language="markdown")

    with tab_khao_thi:
        st.markdown("#### 📝 Prompt Xây dựng Đề kiểm tra & Khảo thí")
        loai_de = st.radio("Chọn cấu trúc đề:", ["Xây dựng toàn bộ Ma trận & Đề kiểm tra", "System Prompt: Thiết lập hệ thống AI Khảo thí"], horizontal=True)
        
        if "toàn bộ" in loai_de:
            st.info("Lệnh tổng hợp tạo từ A-Z một bài kiểm tra kèm Ma trận, Đặc tả, Đề, Đáp án và Hướng dẫn chấm.")
            prompt_de_kt = """NHIỆM VỤ
Hãy xây dựng đầy đủ một Bộ đề kiểm tra môn [Nhập môn học], lớp [Nhập lớp], chủ đề [Nhập chủ đề].

Quy trình:
Bước 1: Phân tích yêu cầu giáo viên.
Bước 2: Sử dụng CT GDPT 2018 (hoặc tài liệu đính kèm nếu có).
Bước 3: Tạo đầy đủ các phần bằng Markdown chuẩn:
I. Ma trận
II. Bản đặc tả
III. Đề kiểm tra (Trắc nghiệm nhiều lựa chọn, Trắc nghiệm Đúng/Sai, Điền khuyết & Tự luận)
IV. Đáp án
V. Hướng dẫn chấm chi tiết

Bước 4: Tự kiểm tra (Review):
✓ Đủ số câu, đủ số điểm, tổng điểm = 10
✓ Đúng tỉ lệ mức độ (Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao)
✓ Không thiếu phần nào. CÁC CÔNG THỨC Toán/Lý/Hóa/Sinh BẮT BUỘC PHẢI DÙNG KÝ HIỆU LATEX (Ví dụ: $$x^2+y^2=1$$)."""
            st.code(prompt_de_kt, language="markdown")
        else:
            st.info("System Prompt giúp thiết lập cấu hình chuyên gia cho các AI tạo đề tự động trong dự án lập trình.")
            prompt_sys = """Bạn là Chuyên gia khảo thí cao cấp của Bộ Giáo dục và Đào tạo Việt Nam.
NHIỆM VỤ
- Xây dựng đề kiểm tra theo Chương trình GDPT 2018.
- Đánh giá phẩm chất và năng lực học sinh.
- Tuân thủ Công văn 5512 và các hướng dẫn khảo thí hiện hành.

QUY TẮC BẮT BUỘC
1. Luôn trả lời bằng định dạng Markdown chuẩn.
2. Công thức Toán, Lý, Hóa, Sinh bắt buộc dùng định dạng LaTeX (VD: $$x^2+y^2=1$$). Tuyệt đối không dùng dấu backtick (`).
3. Bảng Markdown phải đúng chuẩn. Không dùng HTML.
4. Không sinh dữ liệu giả mạo. Không dừng giữa chừng khi xuất văn bản.
5. Chỉ trả về đúng nội dung đề kiểm tra, không giải thích dài dòng dư thừa."""
            st.code(prompt_sys, language="markdown")

    with tab_tinh_huong:
        st.markdown("#### 🧩 Gỡ rối tình huống giảng dạy & Công cụ hỗ trợ")
        th_chon = st.selectbox("Chọn nhu cầu cần xử lý:", [
            "Tạo Phiếu học tập & Câu hỏi thảo luận nhóm",
            "Tóm tắt kiến thức / Sơ đồ hóa",
            "Xử lý tình huống: Học sinh lơ đễnh, mất tập trung",
            "Xử lý tình huống: Xung đột khi làm việc nhóm"
        ])

        if "Phiếu học tập" in th_chon:
            st.code("""Vai trò: Bạn là chuyên gia thiết kế học liệu sư phạm tích cực.
Nhiệm vụ: Hãy thiết kế một Phiếu học tập và 3 câu hỏi thảo luận nhóm (theo kỹ thuật Khăn phủ bàn / Mảnh ghép) cho bài [Điền tên bài], môn [Điền môn].
Yêu cầu:
- Phiếu học tập có phân hóa mức độ rõ ràng: Dành cho HS Cơ bản (Đạt) và HS Nâng cao (Vận dụng sáng tạo).
- Câu hỏi thảo luận phải gắn liền với thực tiễn đời sống để thu hút học sinh.""", language="markdown")
        elif "Tóm tắt" in th_chon:
            st.code("""Vai trò: Bạn là chuyên gia sơ đồ hóa và tóm tắt tư duy.
Nhiệm vụ: Hãy cô đọng kiến thức trọng tâm của bài [Điền tên bài], môn [Điền môn], lớp [Điền lớp].
Yêu cầu: Trình bày dưới dạng bullet points mạch lạc, sử dụng các từ khóa chính (Key terms) hoặc format bảng để giúp học sinh dễ dàng nắm bắt nội dung cốt lõi nhanh nhất trước kỳ thi.""", language="markdown")
        elif "lơ đễnh" in th_chon:
            st.code("""Vai trò: Bạn là chuyên gia tâm lý học đường tuổi vị thành niên.
Nhiệm vụ: Lớp [Điền lớp] của tôi thường xuyên lơ đễnh, mất tập trung và nói chuyện riêng trong giờ [Điền môn]. 
Hãy tư vấn cho tôi: 
1. Ba nguyên nhân tâm lý cốt lõi.
2. Kịch bản 3 bước xử lý mềm mỏng, dứt điểm ngay tại lớp mà không làm gián đoạn hay phá vỡ bầu không khí của tiết học.""", language="markdown")
        else:
            st.code("""Vai trò: Bạn là cố vấn công tác chủ nhiệm chuyên nghiệp.
Nhiệm vụ: Khi thực hiện dự án nhóm bài [Điền bài], học sinh xảy ra tranh cãi nảy lửa, đùn đẩy trách nhiệm và không chịu hợp tác. 
Hãy cung cấp kịch bản giải quyết mâu thuẫn tại chỗ và hướng dẫn cách phân chia lại ma trận vai trò (Team Roles) để rèn luyện kỹ năng hợp tác cho học sinh.""", language="markdown")

    with tab_hs:
        st.markdown("#### 🎓 Hướng dẫn Học sinh sử dụng AI (Tự học & Phản biện)")
        st.info("Giáo viên copy prompt này gửi cho học sinh (hoặc ghim vào group lớp) để định hướng các em dùng AI như một gia sư, đảm bảo tính trung thực.")
        
        hs_chon = st.selectbox("Mục tiêu tự học của học sinh:", [
            "AI là Gia sư gợi mở (Tuyệt đối không giải hộ)",
            "AI là Giáo viên khảo thí luyện tập tương tác",
            "AI là Đối tác phản biện (Luyện Critical Thinking)"
        ])
        
        if "Gia sư" in hs_chon:
            st.code("""Vai trò: Bạn là một gia sư kiên nhẫn, thân thiện và tuân thủ đạo đức giáo dục.
Nhiệm vụ: Tôi là học sinh lớp [Điền lớp]. Tôi đang gặp khó khăn ở bài [Điền tên bài / bài tập].
Nguyên tắc BẮT BUỘC:
- KHÔNG BAO GIỜ được đưa ra đáp án trực tiếp hay giải hộ bài tập cho tôi.
- Hãy dùng phương pháp Socrates: Đặt các câu hỏi gợi mở nhỏ, chia nhỏ vấn đề để dẫn dắt tôi tự suy luận và tự tìm ra đáp án cuối cùng.""", language="markdown")
        elif "luyện tập" in hs_chon:
            st.code("""Vai trò: Bạn là hệ thống trắc nghiệm thông minh.
Nhiệm vụ: Tạo cho tôi 5 câu hỏi ôn tập khách quan về chủ đề [Điền chủ đề].
Cách thức TƯƠNG TÁC (Tuân thủ nghiêm ngặt):
- Chỉ đưa ra TỪNG CÂU HỎI MỘT. 
- Đợi tôi trả lời xong, bạn mới nhận xét đúng/sai, giải thích chi tiết đáp án đó, rồi mới tiếp tục chuyển sang hiển thị câu hỏi tiếp theo.""", language="markdown")
        else:
            st.code("""Vai trò: Bạn là một nhà tư duy phản biện khoa học, sắc bén.
Nhiệm vụ: Tôi có một góc nhìn / ý tưởng về vấn đề: "[Nhập quan điểm của bạn vào đây]".
Hãy đóng vai phản biện (Devil's Advocate): Đặt cho tôi 2-3 câu hỏi lật lại vấn đề, chỉ ra những lỗ hổng logic tiềm ẩn để giúp tôi kiểm tra lại và củng cố lập luận của mình vững chắc hơn.""", language="markdown")

    with tab_ta:
        st.markdown("#### 🇬🇧 Bộ Prompt Chuyên biệt cho Giáo viên Tiếng Anh (ELT)")
        ta_chon = st.selectbox("Chọn Kỹ năng / Hoạt động giảng dạy:", [
            "Tạo bài đọc hiểu (Reading Comprehension Passage)",
            "Luyện từ vựng (Vocabulary Set & Gap-fill)",
            "Chữa lỗi ngữ pháp & Viết (Writing Correction Feedback)",
            "Kịch bản hội thoại thực tế (Speaking Role-play Script)",
            "Trò chơi lớp học (Gamification/Classroom Game)"
        ])
        
        if "đọc hiểu" in ta_chon:
            st.code("""Role: You are an expert English Language Teaching (ELT) material developer.
Task: Create a Reading Comprehension passage for [Target Level: A2/B1/B2] students.
Topic: [Insert Topic]
Requirements:
1. An engaging passage of 150-200 words using appropriate vocabulary and grammar for the level.
2. 5 Multiple-choice questions checking both main ideas and specific details.
3. 3 Open-ended discussion questions for post-reading speaking practice.
4. Provide the full Answer Key at the end.""", language="markdown")
        elif "từ vựng" in ta_chon:
            st.code("""Role: You are an innovative English teacher and curriculum designer.
Task: Create a vocabulary learning set for the topic [Insert Topic] suitable for Grade [Insert Grade] students in Vietnam.
Requirements: 
1. Provide 8-10 key target words/phrases.
2. For each word, include: IPA phonetic transcription, word class, precise Vietnamese meaning, and 1 natural example sentence. 
3. Create a short, context-based gap-fill exercise (with answer key) to practice these new words.""", language="markdown")
        elif "ngữ pháp" in ta_chon:
            st.code("""Role: You are an experienced, encouraging English writing coach.
Task: Analyze the following paragraph written by an ESL student: 
"[Dán đoạn văn tiếng Anh của học sinh vào đây]"
Requirements: 
1. Create a clear table listing errors with columns: (Original Error -> Correction -> Brief Explanation in Vietnamese so the student understands why).
2. Rewrite an improved, natural, and cohesive version of the entire paragraph maintaining the student's original tone.""", language="markdown")
        elif "hội thoại" in ta_chon:
            st.code("""Role: You are a native conversation partner and speaking coach.
Task: Write a natural, modern dialogue for a Speaking role-play activity in an ESL class.
Topic/Situation: [e.g., At a restaurant, Complaining about a product]
Level: [Insert Level: A2/B1]
Requirements:
1. Include Person A and Person B with equal speaking time.
2. Keep the language natural and use 2-3 common idioms/phrasal verbs.
3. Add 3 follow-up discussion questions for pair practice after reading the script.""", language="markdown")
        else:
            st.code("""Role: You are an ELT gamification expert.
Task: Design a fun, fast-paced, low-prep classroom game script to review [Vocabulary/Grammar Topic] for [Grade/Age] students.
Requirements: 
1. Catchy Name of the game.
2. Clear Learning Objectives.
3. Materials needed (keep it minimal).
4. Step-by-step instructions on how to play within a 10-15 minute timeframe. Ensure all students are actively engaged.""", language="markdown")
