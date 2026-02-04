import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import analytics_engine as ae
import db_handler as db
import optimization as opt
import anomaly_detection as ad
import export_handler as exp
import ui_components as ui

# Page configuration
st.set_page_config(
    page_title="Simple Website Analytics Dashboard Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db.init_db()

# Custom styles
ui.apply_custom_styles()

# Sidebar - Settings & Filters
st.sidebar.title("⚙️ Pengaturan & Filter")

language = st.sidebar.radio("Bahasa / Language", ["Indonesia", "English"])
site_name = st.sidebar.text_input("Nama Situs / Site Name", value="My Site")

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Rentang Waktu / Time Range")
today = datetime.now()
start_date = st.sidebar.date_input("Mulai / Start", today - timedelta(days=7))
end_date = st.sidebar.date_input("Selesai / End", today)

st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Privasi / Privacy")
privacy_level = st.sidebar.selectbox("Tingkat Privasi / Privacy Level", ["Low", "Medium", "High", "Anonymize Hash"], index=3)

st.sidebar.markdown("---")
st.sidebar.subheader("🔔 Alert Threshold")
threshold_views = st.sidebar.number_input("Min Views/Hari", value=1000)

# Main Title & Vision
st.title("Simple Website Analytics Dashboard Optimizer")
st.markdown(f"**Visi:** Membantu blogger dan usaha kecil Indonesia dengan analitik esensial yang fokus pada privasi.")

# Warning Box
warning_text_id = "Estimasi kasar, data anonymized, bukan pengganti analytics full, konsultasi profesional direkomendasikan."
warning_text_en = "Rough estimation, anonymized data, not a replacement for full analytics, professional consultation recommended."
st.markdown(f'<div class="warning-box">{warning_text_id if language == "Indonesia" else warning_text_en}</div>', unsafe_allow_html=True)

# Tabs
tab_dash, tab_opt, tab_scenario, tab_export, tab_vision = st.tabs([
    "Dashboard", "Optimization", "Scenario Simulation", "Export", "Vision"
])

# Dummy Data Load
df_history, summary = ae.get_dummy_metrics()

with tab_dash:
    st.header("📊 Real-Time Tracking & Insights")
    
    # Metrics Rows
    col1, col2, col3, col4 = st.columns(4)
    
    # Confidence Interval
    ci = ad.calculate_confidence_interval(df_history['Visitors'])
    
    with col1:
        st.metric("Unique Visitors", f"{summary['total_visitors']}", f"±{ci:.1f}")
    with col2:
        st.metric("Avg Session Time", f"{summary['avg_session_time']}s", "Next: 130s")
    with col3:
        st.metric("Bounce Rate", f"{summary['avg_bounce_rate']}%", "-2%", delta_color="inverse")
    with col4:
        spike_color = "normal" if summary['spike_status'] is None else "off"
        st.metric("Alert Status", summary['spike_status'] or "Normal", delta=None)

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        ui.render_line_chart(df_history, 'Date', 'Visitors', "Tren Pengunjung (Visitor Trend)")
    with c2:
        sources = ['Organic', 'Direct', 'Referral', 'Social']
        counts = [45, 25, 20, 10]
        ui.render_pie_chart(sources, counts, "Sumber Trafik (Traffic Sources)")

    # Recent Pages
    st.subheader("Halaman Teratas (Top Pages)")
    top_pages = pd.DataFrame({
        'Page': ['/home', '/blog/tips-seo', '/product/optimizer', '/contact'],
        'Views': [2500, 1200, 850, 200],
        'Bounce': ['40%', '55%', '45%', '85%']
    })
    st.table(top_pages)

with tab_opt:
    st.header("🎯 Content Focus Recommendations")
    pages, views, bounces = opt.get_dummy_optimization_data()
    recs = opt.optimize_content_performance(pages, views, bounces)
    
    for r in recs:
        st.success(f"**Fokus pada halaman: {r['page']}**")
        st.write(f"Views: {r['views']}, Bounce Rate: {r['bounce_rate']}%")
        st.write(f"Saran: {r['suggestion']}")
        st.markdown("---")

with tab_scenario:
    st.header("🧪 Scenario Simulation (What-If)")
    st.write("Ubah parameter untuk melihat estimasi dampak pada metrik.")
    
    sim_views = st.slider("Target Views Tambahan (%)", -50, 200, 20)
    sim_bounce = st.slider("Target Penurunan Bounce Rate (%)", -50, 50, 5)
    
    new_visitors = summary['total_visitors'] * (1 + sim_views/100)
    new_bounce = summary['avg_bounce_rate'] * (1 - sim_bounce/100)
    
    st.info(f"Proyeksi Pengunjung Baru: **{int(new_visitors)}**")
    st.info(f"Proyeksi Bounce Rate Baru: **{new_bounce:.1f}%**")
    
    # Anomaly Prediction
    pred_val, is_anom = ad.predict_trends(df_history['Visitors'].values)
    st.subheader("AI Anomaly Prediction")
    st.write(f"Prediksi pengunjung hari esok: **{int(pred_val)}**")
    if is_anom:
        st.warning("⚠️ Anomali terdeteksi berdasarkan variasi data terakhir!")
    else:
        st.success("✅ Tren stabil sesuai ekspektasi linear.")

with tab_export:
    st.header("📥 Export Reports")
    
    export_format = st.radio("Pilih Format Ekspor", ["CSV", "Excel", "PDF"])
    
    if st.button("Generate & Download"):
        if export_format == "CSV":
            data = exp.export_to_csv(df_history)
            st.download_button("Download CSV", data, "analytics_report.csv", "text/csv")
        elif export_format == "Excel":
            data = exp.export_to_excel(df_history)
            st.download_button("Download Excel", data, "analytics_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif export_format == "PDF":
            report_data = {
                'site_name': site_name,
                'total_visitors': summary['total_visitors'],
                'avg_bounce_rate': summary['avg_bounce_rate'],
                'avg_session_time': summary['avg_session_time'],
                'recommendations': [r['page'] + ": " + r['suggestion'] for r in recs]
            }
            data = exp.export_to_pdf(report_data)
            st.download_button("Download PDF", data, "analytics_report.pdf", "application/pdf")

with tab_vision:
    st.header("🌐 Project Vision")
    st.write("""
    **Simple Website Analytics Dashboard Optimizer** adalah langkah awal untuk memberikan solusi analitik 
    yang terjangkau dan etis bagi ekosistem digital di Indonesia. 
    
    Fokus kami pada:
    - **Digital Sovereignty**: Data tidak keluar ke pihak ketiga yang haus data.
    - **Anti-Bloat**: Hanya metrik yang benar-benar Anda perlukan untuk tumbuh.
    - **2026 Ready**: Siap dengan regulasi privasi data yang semakin ketat di masa depan.
    
    *Scale Potential:* Enterprise vertical analytics, AI-driven anomaly detection, dan integrasi SEO tools.
    """)
    
    st.subheader("Potensi Integrasi Masa Depan")
    st.code("""
<!-- Install Snippet Placeholder -->
<script src="https://analytics.aryhh.com/tracker.js" data-site="MY_SITE_ID" async></script>
    """, language='html')
    
    st.markdown("""
    - **WordPress/Shopify**: Plugin integrasi satu klik.
    - **Google Sheets / Zapier**: Otomatisasi alur kerja laporan.
    - **Ahrefs/SEO Bundling**: Menggabungkan data on-site dengan off-site insights.
    """)

# Footer
ui.render_footer()
