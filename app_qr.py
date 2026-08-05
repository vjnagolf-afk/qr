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

st.markdown("""
    <div class="main-header">
        <h1>🎓 TRƯỜNG THCS NGUYỄN CHÍ THANH</h1>
        <p>⚡ Trợ lý Tạo Mã QR Sạch & Tùy Biến Tên Giáo Viên</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎨 Tùy chỉnh phong cách QR")
qr_color = st.sidebar.color_picker("Chọn màu cho mã QR:", "#162447")
bg_color = st.sidebar.color_picker("Chọn màu nền QR:", "#ffffff")
box_size_val = st.sidebar.slider("Độ phân giải mã QR (Kích thước ảnh):", min_value=6, max_value=15, value=10)

st.sidebar.markdown("---")
st.sidebar.markdown("### ✍️ Tùy chỉnh chữ tên tác giả")
custom_font_size = st.sidebar.slider("Chọn cỡ chữ (Pixel):", min_value=10, max_value=80, value=24)
banner_height_val = st.sidebar.slider("Chiều cao khung chứa chữ:", min_value=30, max_value=120, value=60)

st.markdown("### 📥 Nhập thông tin & Tên tác giả")
target_link = st.text_input(
    "Dán đường link bất kỳ:",
    placeholder="VD: https://thcsnguyenchithanh-lhd.streamlit.app/..."
)

creator_name = st.text_input(
    "Tên người tạo / Giáo viên (Hỗ trợ tiếng Việt có dấu):",
    placeholder="VD: Thầy Lê Hồng Dương"
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
                
                # Danh sách đường dẫn font hỗ trợ tiếng Việt trên Linux/Cloud hoặc Windows
                font_paths = [
                    "DejaVuSans.ttf",
                    "DejaVuSans-Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "arial.ttf",
                    "angsana.ttc"
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
                
                text_to_display = f"Tác giả: {creator_name.strip()}"
                
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
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("#### 📱 Mã QR Tùy Biến Của Bạn:")
                st.image(buf.getvalue(), caption="Quét mã để truy cập trực tiếp", use_container_width=True)
                
                st.download_button(
                    label="📥 TẢI ẢNH MÃ QR HOÀN CHỈNH (.PNG)",
                    data=buf.getvalue(),
                    file_name="ma_qr_giao_vien_chuyen_nghiep.png",
                    mime="image/png",
                    type="primary"
                )
        except Exception as e:
            st.error(f"⚠️ Có lỗi xảy ra: {e}")
    else:
        st.error("⚠️ Máy chủ chưa cài đặt thư viện cần thiết.")
else:
    st.info("💡 Thầy/Cô hãy nhập thông tin và kiểm tra lại tên tiếng Việt có dấu nhé!")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Được thiết kế riêng phục vụ công tác chuyên môn - Trường THCS Nguyễn Chí Thanh 🏫</p>",
    unsafe_allow_html=True
)
