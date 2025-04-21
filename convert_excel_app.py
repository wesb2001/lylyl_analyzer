import streamlit as st
import pandas as pd
import tempfile
import os
from auto_convert_excel import convert_excel_file

def main():
    st.set_page_config(page_title="LYLYL 광고 성과 자동 변환기", layout="centered")
    st.title("📊 LYLYL 광고 성과 자동 변환기")
    st.markdown("""
    이 앱은 메타 광고 리포트 엑셀 파일을 최종 분석 포맷으로 자동 변환해줍니다.
    - 광고비 0원 항목 제거
    - 후크, 지속 자동 계산
    - ROAS, CPC, CVR, CTR 서식 적용
    - CVR 100 이상 보정 포함
    """)

    uploaded_file = st.file_uploader("📁 원본 엑셀 파일 업로드", type=["xlsx"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_input:
            tmp_input.write(uploaded_file.read())
            input_path = tmp_input.name

        output_path = input_path.replace(".xlsx", "_변환완료.xlsx")
        convert_excel_file(input_path, output_path)

        with open(output_path, "rb") as f:
            st.success("✅ 변환 완료! 아래에서 파일을 다운로드하세요.")
            st.download_button(
                label="📥 변환된 엑셀 파일 다운로드",
                data=f,
                file_name="LYLYL_광고_분석_결과.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # 정리
        os.remove(input_path)
        os.remove(output_path)

if __name__ == "__main__":
    main()
