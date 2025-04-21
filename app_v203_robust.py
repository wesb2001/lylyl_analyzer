
import streamlit as st
import pandas as pd

st.set_page_config(page_title="LYLYL 광고 자동 분석기", layout="centered")

st.title("📊 LYLYL 광고 자동 분석기")
st.caption("메타 광고 데이터만 업로드해도 자동 분석됩니다. (템플릿은 선택 사항입니다)")

meta_file = st.file_uploader("메타 광고 데이터 (.xlsx)", type=["xlsx"])
template_file = st.file_uploader("분석 템플릿 파일 (.xlsx, 선택)", type=["xlsx"])

if meta_file:
    df_meta = pd.read_excel(meta_file)

    # ✅ 자동 열 보정
    if "CTR" not in df_meta.columns:
        st.warning("📌 CTR 열이 없어 0으로 채웁니다.")
        df_meta["CTR"] = 0.0

    if "후크" not in df_meta.columns:
        st.warning("📌 후크 열이 없어 0으로 채웁니다.")
        df_meta["후크"] = 0.0

    if "지속" not in df_meta.columns:
        st.warning("📌 지속 열이 없어 0으로 채웁니다.")
        df_meta["지속"] = 0.0

    # ROAS 계산 (구매 / 광고비)
    if "매출" in df_meta.columns and "광고비" in df_meta.columns:
        df_meta["ROAS"] = (df_meta["매출"] / df_meta["광고비"]).round(2)
    else:
        st.warning("ROAS 계산을 위한 '매출' 또는 '광고비' 열이 없습니다.")

    st.success("✅ 데이터 업로드 및 보정 완료!")
    st.dataframe(df_meta)

    # 템플릿 적용 시 분석 결과 병합
    if template_file:
        df_template = pd.read_excel(template_file)
        df_template["제목_norm"] = df_template["제목"].str.strip().str.lower().str.replace(" ", "")
        df_meta["제목_norm"] = df_meta["제목"].str.strip().str.lower().str.replace(" ", "")
        merged = pd.merge(df_template, df_meta, on="제목_norm", how="left")
        st.write("📎 템플릿 병합 결과:")
        st.dataframe(merged)
