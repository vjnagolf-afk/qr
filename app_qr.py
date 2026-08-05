# -*- coding: utf-8 -*-
import streamlit as st
import io

try:
    import qrcode
    from PIL import Image, ImageColor
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

# Cấu hình trang
st.set_page_config(
    page_title="Trang Tạo Mã QR Sạch - THCS Nguyễn Chí Thanh",
    page_icon="🎓",
    layout="centered"
)

# Tùy chỉnh giao diện CSS (Tạo hiệu ứng màu sắc, bo góc, tiêu đề sinh động)
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

# Tiêu đề giao diện chính mang phong cách riêng
st.markdown("""
    <div class="main-header">
        <h1>🎓 TRƯỜNG THCS NGUYỄN CHÍ THANH</h1>
        <p>⚡ Trợ lý Tạo Mã QR Sạch & Chuyên Nghiệp Cho Giáo Viên</p>
    </div>
""", unsafe_allow_html=True)

# Phần cấu hình nâng cao trong sidebar (Giúp giáo viên tùy chỉnh màu sắc mã QR theo sở thích)
st.sidebar.markdown("### 🎨 Tùy chỉnh phong cách QR")
qr_color = st.sidebar.color_picker("Chọn màu cho mã QR:", "#162447")
bg_color = st.sidebar.color_picker("Chọn màu nền QR:", "#ffffff")

box_size_val = st.sidebar.slider("Độ phân giải (Kích thước):", min_value=6, max_value=15, value=10)

st.markdown("### 📥 Nhập thông tin liên kết")
target_link = st.text_input(
    "Dán đường link bất kỳ (Bài giảng, Quizizz, Website, tài liệu...):",
    placeholder="VD: https://thcsnguyenchithanh-lhd.streamlit.app/..."
)

if target_link:
    if HAS_QRCODE:
        try:
            # Khởi tạo tạo mã QR với các thông số tùy chọn từ sidebar
            qr = qrcode.QRCode(
                version=1,
                box_size=box_size_val,
                border=4
            )
            qr.add_data(target_link)
            qr.make(fit=True)
            
            # Tạo hình ảnh mã QR với màu sắc tùy chỉnh
            img_qr = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')
            
            # Xuất ra bộ nhớ đệm
            buf = io.BytesIO()
            img_qr.save(buf, format="PNG")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("#### 📱 Mã QR của bạn:")
                st.image(buf.getvalue(), caption="Quét mã để truy cập trực tiếp", use_container_width=True)
                
                # Nút tải ảnh QR về máy
                st.download_button(
                    label="📥 TẢI ẢNH MÃ QR (.PNG)",
                    data=buf.getvalue(),
                    file_name="ma_qr_giao_vien_thcs_nct.png",
                    mime="image/png",
                    type="primary"
                )
        except Exception as e:
            st.error(f"⚠️ Có lỗi xảy ra khi khởi tạo mã QR: {e}")
    else:
        st.error("⚠️ Máy chủ chưa cài đặt thư viện tạo QR. Vui lòng kiểm tra lại file `requirements.txt`.")
else:
    st.info("💡 **Mẹo:** Thầy/Cô có thể tùy chỉnh màu sắc mã QR ở thanh công cụ bên trái (`>`) để phù hợp với phong cách cá nhân trước khi tải về!")

# Chân trang (Footer)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Được thiết kế riêng phục vụ công tác chuyên môn - Trường THCS Nguyễn Chí Thanh 🏫</p>",
    unsafe_allow_html=True
)
