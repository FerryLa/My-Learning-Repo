# ENEX 기반 유사 뉴스 크롤링 파이프라인

당신이 ENEX에 스크랩한 "중요 뉴스"를 기준으로, **유사한 최신 기사**만 찾아 텔레그램으로 보내는 최소 구현체입니다.

## 구성
- `config.yaml`: RSS 시드, 임계치, 배치 크기 등 설정
- `data/evernote_export_parsed.csv`: ENEX 파싱 결과 (이미 있으니 경로만 맞추면 됩니다)
- `src/`
  - `enex_prototypes.py`: ENEX 텍스트로 주제 클러스터의 프로토타입 벡터 계산
  - `crawl_rss.py`: RSS로 최신 기사 후보 수집
  - `extract_text.py`: URL에서 본문 추출
  - `embed.py`: 임베딩 계산. `sentence-transformers` 있으면 사용, 없으면 TF-IDF fallback
  - `similarity.py`: 코사인 유사도, MMR 다양성, 중복 필터
  - `telegram_client.py`: 텔레그램 전송
  - `run_pipeline.py`: 전체 파이프라인 오케스트레이터

## 설치
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
옵션: GPU/모델 최적화는 알아서 행복한 선택을 하세요.

## 환경변수
- `TELEGRAM_BOT_TOKEN`: 텔레그램 봇 토큰
- `TELEGRAM_CHAT_ID`: 메시지를 보낼 채팅 ID

(테스트는 전용 비공개 채널에서 하세요. 실수로 전사에 뉴스 폭탄 터뜨리지 말고요.)

## 실행
1) `config.yaml`에서 `rss_feeds`를 채우세요. ENEX에서 상위 도메인만 뽑아도 시작 가능합니다.
2) `data/evernote_export_parsed.csv` 경로가 맞는지 확인.
3) 파이프라인 실행:
```bash
python -m src.run_pipeline --config config.yaml
```
기본은 2회/일 배치에 맞춘 구성입니다. 스케줄러는 `cron`이나 작업 스케줄러 쓰면 됩니다.

## 아이디어/확장
- 분류기 추가(약한 라벨): `embed + meta` 피처로 로지스틱/LightGBM
- 한국어 요약: 규칙 기반 핵심문장 2~3개 → 필요시 모델 요약으로 교체
- 중복 감시: URL 정규화 + 내용 임베딩 근접

이 레포는 **현실적으로 빨리 결과 보는** 버전입니다. 텔레그램 포맷은 짧고 일정하게 유지하세요.
