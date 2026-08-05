# -*- coding: utf-8 -*-
import streamlit as st
import io

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

# Cấu hình trang
st.set_page_config(
    page_title="Trang Tạo Mã QR Sạch - THCS Nguyễn Chí Thanh",
    page_icon="🎓",
    layout="centered"
)

# Tùy chỉnh giao diện CSS
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1f4068 0%, #162447 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
    }
    .main-header p {
        margin: 8px 0 0 0;
        font-size: 14px;
        color: #e4e4e4;
    }
    .stButton>button {
        width: 100%;
        background-color: #0f4c81;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #1b6ca8;
    }
    </style>
""", unsafe_allow_html=True)

# Tiêu đề giao diện chính
st.markdown("""
    <div class="main-header">
        <h1>🎓 TRƯỜNG THCS NGUYỄN CHÍ THANH</h1>
        <p>⚡ Trợ lý Tạo Mã QR Sạch & Tùy Biến Tên Giáo Viên</p>
    </div>
""", unsafe_allow_html=True)

# Phần cấu hình tùy chỉnh trong sidebar
st.sidebar.markdown("### 🎨 Tùy chỉnh phong cách QR")
qr_color = st.sidebar.color_picker("Chọn màu cho mã QR:", "#162447")
bg_color = st.sidebar.color_picker("Chọn màu nền QR:", "#ffffff")
box_size_val = st.sidebar.slider("Độ phân giải (Kích thước):", min_value=8, max_value=15, value=10)

st.markdown("### 📥 Nhập thông tin & Tên tác giả")
target_link = st.text_input(
    "Dán đường link bất kỳ:",
    placeholder="VD: https://thcsnguyenchithanh-lhd.streamlit.app/..."
)

# Thêm ô nhập tên người tạo / tên giáo viên để gắn trực tiếp lên QR
creator_name = st.text_input(
    "Tên người tạo / Giáo viên (Hiển thị ngay trên ảnh QR):",
    placeholder="VD: Thầy Lê Hồng Dương"
)

if target_link:
    if HAS_QRCODE:
        try:
            # Khởi tạo tạo mã QR
            qr = qrcode.QRCode(
                version=2,  # Tăng version để có đủ không gian cho chữ
                error_correction=qrcode.constants.ERROR_CORRECT_H, # Mức độ sửa lỗi cao để chèn chữ/ảnh an toàn
                box_size=box_size_val,
                border=4
            )
            qr.add_data(target_link)
            qr.make(fit=True)
            
            # Tạo hình ảnh mã QR cơ bản
            img_qr = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')
            
            # Nếu người dùng có nhập tên, tiến hành ghép thêm băng thông chứa tên ở phía dưới mã QR
            if creator_name.strip():
                qr_width, qr_height = img_qr.size
                banner_height = 50 # Chiều cao của khung chứa tên
                
                # Tạo bức ảnh mới lớn hơn để chứa cả mã QR và khung tên bên dưới
                new_img = Image.new("RGB", (qr_width, qr_height + banner_height), color=bg_color)
                new_img.paste(img_qr, (0, 0))
                
                # Vẽ chữ lên khung
                draw = ImageDraw.Draw(new_img)
                try:
                    # Cố gắng sử dụng font mặc định hệ thống
                    font = ImageFont.load_default()
                except:
                    font = None
                
                # Tính toán vị trí đặt chữ ở giữa khung dưới
                text_to_display = f"Tác giả: {creator_name.strip()}"
                
                # Vẽ nền chữ hoặc đường kẻ phân cách cho sinh động
                draw.rectangle([(0, qr_height), (qr_width, qr_height + banner_height)], fill=qr_color)
                
                # Tải màu chữ trắng nổi bật trên nền màu của QR
                # Dùng textbbox để căn giữa chữ
                bbox = draw.textbbox((0, 0), text_to_display, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                
                text_x = (qr_width - text_w) / 2
                text_y = qr_height + (banner_height - text_h) / 2
                
                draw.text((text_x, text_y), text_to_display, fill="#ffffff", font=font)
                final_img = new_img
            else:
                final_img = img_qr

            # Xuất ra bộ nhớ đệm để hiển thị và tải về
            buf = io.BytesIO()
            final_img.save(buf, format="PNG")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("#### 📱 Mã QR Tùy Biến Của Bạn:")
                st.image(buf.getvalue(), caption="Quét mã để truy cập trực tiếp", use_container_width=True)
                
                # Nút tải ảnh QR về máy
                st.download_button(
                    label="📥 TẢI ẢNH MÃ QR CÓ TÊN (.PNG)",
                    data=buf.getvalue(),
                    file_name="ma_qr_giao_vien_chuyen_nghiep.png",
                    mime="image/png",
                    type="primary"
                )
        except Exception as e:
            st.error(f"⚠️ Có lỗi xảy ra khi tạo mã QR: {e}")
    else:
        st.error("⚠️ Máy chủ chưa cài đặt thư viện cần thiết.")
else:
    st.info("💡 Thầy/Cô hãy nhập đường link và điền tên của mình vào ô phía trên để mã QR hiển thị trực tiếp tên tác giả!")

# Chân trang (Footer)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Được thiết kế riêng phục vụ công tác chuyên môn - Trường THCS Nguyễn Chí Thanh 🏫</p>",
    unsafe_allow_html=True
)
