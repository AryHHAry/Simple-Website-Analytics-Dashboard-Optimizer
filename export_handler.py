import pandas as pd
from fpdf import FPDF
import io

def export_to_csv(df):
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def export_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def export_to_pdf(summary_data):
    """
    summary_data: dict with key stats
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Simple Website Analytics Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Site Name: {summary_data.get('site_name', 'My Site')}", ln=True)
    pdf.cell(200, 10, txt=f"Total Visitors: {summary_data.get('total_visitors', 0)}", ln=True)
    pdf.cell(200, 10, txt=f"Avg Bounce Rate: {summary_data.get('avg_bounce_rate', 0)}%", ln=True)
    pdf.cell(200, 10, txt=f"Avg Session Time: {summary_data.get('avg_session_time', 0)}s", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Actionable Recommendations:", ln=True)
    pdf.set_font("Arial", size=10)
    for rec in summary_data.get('recommendations', []):
        pdf.multi_cell(0, 10, txt=f"- {rec}")
    
    return pdf.output(dest='S').encode('latin-1')
