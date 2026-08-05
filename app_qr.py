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
box_size_val = st.sidebar.slider("Độ phân giải mã QR (Kích thước ảnh):", min_value=6, max_value=20, value=12)

# Tùy chỉnh tỷ lệ chữ tác giả
st.sidebar.markdown("---")
st.sidebar.markdown("### ✍️ Tùy chỉnh chữ tên tác giả")
font_scale_val = st.sidebar.slider("Tỷ lệ cỡ chữ (% so với khung):", min_value=10, max_value=50, value=28)

st.markdown("### 📥 Nhập thông tin & Tên tác giả")
target_link = st.text_input(
    "Dán đường link bất kỳ:",
    placeholder="VD: https://thcsnguyenchithanh-lhd.streamlit.app/..."
)

# Ô nhập tên người tạo / tên giáo viên
creator_name = st.text_input(
    "Tên người tạo / Giáo viên (Hiển thị ngay trên ảnh QR):",
    placeholder="VD: Thầy Lê Hồng Dương"
)

if target_link:
    if HAS_QRCODE:
        try:
            # Khởi tạo tạo mã QR
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=box_size_val,
                border=4
            )
            qr.add_data(target_link)
            qr.make(fit=True)
            
            # Tạo hình ảnh mã QR cơ bản
            img_qr = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')
            
            if creator_name.strip():
                qr_width, qr_height = img_qr.size
                
                # Tự động tính chiều cao khung chữ và cỡ chữ dựa trên độ rộng thực tế của ảnh QR
                # Điều này giúp ảnh ở độ phân giải nào thì chữ cũng tự động to đẹp tương ứng
                banner_height_val = int(qr_width * 0.15) # Chiều cao khung bằng 15% bề ngang QR
                dynamic_font_size = int(banner_height_val * (font_scale_val / 50.0))
                if dynamic_font_size < 10: dynamic_font_size = 10

                # Tạo ảnh mới chứa QR và khung tên bên dưới
                new_img = Image.new("RGB", (qr_width, qr_height + banner_height_val), color=bg_color)
                new_img.paste(img_qr, (0, 0))
                
                draw = ImageDraw.Draw(new_img)
                
                # Nạp font chữ theo tỷ lệ tính toán
                try:
                    font = ImageFont.truetype("arial.ttf", dynamic_font_size)
                except:
                    try:
                        font = ImageFont.truetype("DejaVuSans-Bold.ttf", dynamic_font_size)
                    except:
                        font = ImageFont.load_default()
                
                text_to_display = f"Tác giả: {creator_name.strip()}"
                
                # Vẽ khung nền chứa tên
                draw.rectangle([(0, qr_height), (qr_width, qr_height + banner_height_val)], fill=qr_color)
                
                # Căn giữa chữ trong khung
                bbox = draw.textbbox((0, 0), text_to_display, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                
                text_x = (qr_width - text_w) / 2
                text_y = qr_height + (banner_height_val - text_h) / 2
                
                draw.text((text_x, text_y), text_to_display, fill="#ffffff", font=font)
                final_img = new_img
            else:
                final_img = img_qr

            # Xuất ra bộ nhớ đệm
            buf = io.BytesIO()
            final_img.save(buf, format="PNG")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("#### 📱 Mã QR Tùy Biến Của Bạn:")
                st.image(buf.getvalue(), caption="Quét mã để truy cập trực tiếp", use_container_width=True)
                
                # Nút tải ảnh QR về máy
                st.download_button(
                    label="📥 TẢI ẢNH MÃ QR HOÀN CHỈNH (.PNG)",
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
    st.info("💡 Thầy/Cô hãy nhập đường link, điền tên và tùy chỉnh tỷ lệ chữ ở bên trái nhé!")

# Chân trang (Footer)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Được thiết kế riêng phục vụ công tác chuyên môn - Trường THCS Nguyễn Chí Thanh 🏫</p>",
    unsafe_allow_html=True
)
