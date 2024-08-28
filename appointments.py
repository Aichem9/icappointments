import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 제목 설정
st.title("학부모 상담 예약 시스템")

# 현재 날짜를 기준으로 날짜 범위를 설정
today = datetime.today()
min_date = today + timedelta(days=1)  # 오늘 다음 날부터 예약 가능
max_date = today + timedelta(days=14)  # 오늘부터 14일 후까지 예약 가능

# 입력 폼 생성
with st.form(key='appointment_form'):
    parent_name = st.text_input("학부모님 성함", max_chars=30)
    student_name = st.text_input("학생 이름", max_chars=30)
    contact_number = st.number_input("연락처", min_value=1000000000, max_value=9999999999999, step=1)
    appointment_date = st.date_input("상담 희망일", min_value=min_date, max_value=max_date)
    appointment_time = st.time_input("상담 희망 시간")
    notes = st.text_area("비고", help="추가로 전하고 싶은 말씀이 있으면 적어주세요.")

    # 폼 제출 버튼
    submit_button = st.form_submit_button(label="상담 예약하기")

# 폼이 제출되었을 때의 동작
if submit_button:
    # 입력 데이터를 데이터프레임으로 변환
    new_appointment = pd.DataFrame({
        '학부모님 성함': [parent_name],
        '학생 이름': [student_name],
        '연락처': [str(contact_number)],  # 숫자를 문자열로 변환하여 저장
        '상담 희망일': [appointment_date.strftime('%Y-%m-%d')],
        '상담 희망 시간': [appointment_time.strftime('%H:%M')],
        '비고': [notes]
    })

    # 기존 데이터가 있는지 확인하고 파일에 추가 저장
    try:
        existing_appointments = pd.read_csv('appointments.csv')
        updated_appointments = pd.concat([existing_appointments, new_appointment], ignore_index=True)
    except FileNotFoundError:
        updated_appointments = new_appointment

    # 데이터를 CSV 파일로 저장
    updated_appointments.to_csv('appointments.csv', index=False)

    # 성공 메시지 출력
    st.success("상담 예약이 완료되었습니다!")

# 예약된 상담 내역 확인 버튼
if st.button('예약된 상담 내역 보기'):
    try:
        appointments = pd.read_csv('appointments.csv')
        st.dataframe(appointments)
    except FileNotFoundError:
        st.warning("예약된 상담 내역이 없습니다.")
