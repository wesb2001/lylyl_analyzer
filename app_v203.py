
import streamlit as st
import pandas as pd

st.set_page_config(page_title="LYLYL 광고 자동 분석기", page_icon="📊", layout="centered")

st.title("📊 LYLYL 광고 자동 분석기")
st.markdown("메타 광고 데이터만 업로드해도 자동 분석됩니다. (템플릿은 선택 사항입니다)")

meta_file = st.file_uploader("1. 메타 광고 데이터 (.xlsx)", type=["xlsx"])
template_file = st.file_uploader("2. 분석 템플릿 파일 (.xlsx, 선택)", type=["xlsx"])

if meta_file:
    df_meta = pd.read_excel(meta_file)

    def normalize(text):
        return str(text).strip().lower().replace(" ", "").replace("_", "").replace("\n", "")

    df_meta.columns = [normalize(col) for col in df_meta.columns]

    df_result = df_meta.copy()

    # ROAS 수식 삽입 (E:매출, C:광고비 열 기준)
    for i in range(len(df_result)):
        row_num = i + 2
        df_result.at[i, "roas"] = f"=e{row_num}/c{row_num}"

    # 계산 컬럼 추가
    try:
        df_result["ctr"] = df_result["ctr"] * 0.01
        df_result["후크"] = (df_result["동영상3초이상재생"] / df_result["동영상재생"]).round(4)
        df_result["지속"] = (df_result["동영상100%재생"] / df_result["동영상3초이상재생"]).round(4)
    except KeyError as e:
        st.error(f"⚠️ 필요한 열이 누락되어 분석할 수 없습니다: {e}")
        st.stop()

    st.success("✅ 분석 완료! 아래에서 결과를 미리 보고 다운로드하세요.")
    st.dataframe(df_result.head())

    csv = df_result.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 결과 다운로드 (.csv)",
        data=csv,
        file_name="LYLYL_광고_분석결과.csv",
        mime="text/csv"
    )
else:
    st.info("먼저 메타 광고 데이터를 업로드해 주세요.")
