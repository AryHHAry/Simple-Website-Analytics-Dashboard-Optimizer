import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def apply_custom_styles():
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #ffffff;
            color: #666;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            border-top: 1px solid #eee;
        }
        .warning-box {
            padding: 10px;
            border-radius: 5px;
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_line_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df[x_col], df[y_col], marker='o', linestyle='-', color='#007bff')
    ax.set_title(title, fontsize=14, fontweight='bold', color='#333')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def render_bar_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df[x_col], df[y_col], color='#28a745')
    ax.set_title(title, fontsize=14, fontweight='bold', color='#333')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    st.pyplot(fig)

def render_pie_chart(labels, sizes, title):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax.axis('equal') 
    plt.title(title, fontweight='bold')
    st.pyplot(fig)

def render_footer():
    st.markdown("""
        <div class="footer">
            Created by Ary HH (aryhharyanto@proton.me) – Untuk simple website analytics dashboard optimizer Indonesia
        </div>
    """, unsafe_allow_html=True)
