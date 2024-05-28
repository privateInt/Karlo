# 프로젝트 목적

- 사용자 입력값(키워드, 화풍, 구도)을 text2img API(kakao brain Karlo)에 전달하여 해당 이미지 생성

# 실험 내용

## model

- naver hyper clova API인 HCX-003, HCX-DASH-001 모델을 비교 분석함
- 분석 결과 HCX-003의 비용, 추론 속도 등은 HCX-DASH-001에 비해 부족했지만, 감당 가능한 수준이었음
- 분석 결과 HCX-DASH-001은 톤앤매너의 분위기 이해 등 품질면에서 부족한 수준이었음
- HCX-003 모델 결정

## parameter

- 품질에 영향을 미치는 parameter의 수치를 변화하는 방식으로 parameter의 영향 파악
- temperature 0.5 결정

# 환경 설치

```sh
pip install -r requirements.txt
```

# 데모 페이지 실행

```sh
streamlit run Ncopy_test_demo.py
```

# 데모 페이지 예시

![Cap 2024-05-28 15-33-02-851](https://github.com/privateInt/Karlo/assets/95892797/877aa2da-1497-44ef-83ec-3ee197b7e9f8)

![Cap 2024-05-28 15-33-25-957](https://github.com/privateInt/Karlo/assets/95892797/93f756b7-8e62-419e-8a97-7418091cc8ae)

![Cap 2024-05-28 15-33-30-860](https://github.com/privateInt/Karlo/assets/95892797/cc39bbe5-09aa-4e1d-8b60-fae9999a2787)

![Cap 2024-05-28 15-33-37-535](https://github.com/privateInt/Karlo/assets/95892797/7b213d76-992e-45b9-9973-d07628aecf5b)

![Cap 2024-05-28 15-33-43-357](https://github.com/privateInt/Karlo/assets/95892797/29c9947e-cbb2-4afe-91fb-f768c807fca0)
