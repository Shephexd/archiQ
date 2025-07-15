# ArchiQ - AWS 아키텍처 리뷰 도구

ArchiQ는 Amazon Q Developer와 통합되어 고객의 현재 AWS 아키텍처를 자동으로 분석하고 개선 방안을 제시하는 도구입니다. 서울 리전 최적화 및 간소화된 사용자 경험을 제공합니다.

## 🚀 주요 기능

### 1. Service Screener 결과 기반 Well-Architected Review
- 특정 디렉토리의 Service Screener 결과 파일을 분석
- Well-Architected Framework 6개 기둥 기반 종합 평가
- 우선순위별 개선 권장사항 제시

### 2. AWS 리소스 기반 보안 점검
- 실제 AWS 리소스를 스캔하여 보안 위험 요소 식별
- 네트워크 보안, 접근 제어, 데이터 보호 등 종합 분석
- 구체적인 보안 강화 방안 제시

### 3. AWS 리소스 기반 Well-Architected 리뷰
- 현재 운영 중인 AWS 리소스 기반 아키텍처 분석
- 6개 기둥별 상세 평가 및 점수 산정
- Mermaid 다이어그램을 포함한 시각적 아키텍처 표현

### 4. AWS 리소스 기반 아키텍처 다이어그램 생성
- 현재 AWS 환경의 아키텍처를 자동으로 시각화
- Mermaid 및 draw.io 호환 형식 제공
- 다중 레벨 다이어그램 (High-Level, Network-Level, Service-Level)

## 🔧 핵심 기술 특징

### Hanging 문제 해결
- **자동 응답 시스템**: `qchat chat --trust-all-tools`의 y/n/t 프롬프트 자동 처리
- **안정적인 프로세스 관리**: `communicate()` 방식으로 안정성 확보
- **간단한 구조**: 복잡한 예외 처리 제거하고 핵심 기능에 집중

## 📁 프로젝트 구조

```
/home/ec2-user/archiQ
├── src/
│   ├── cli.py                    # 🎯 ArchiQ 메인 CLI 인터페이스
│   ├── middleware/               # Amazon Q Developer 통합 레이어
│   │   └── amazon_q_hook.py     # 🔧 간소화된 Interactive Session 핸들러
│   └── prompt/                   # 🎨 기능별 프롬프트 템플릿
│       ├── service_screener_review.md
│       ├── security_check.md
│       ├── well_architected_review.md
│       └── architecture_diagram.md
├── output/                       # 📊 생성된 HTML 보고서 저장소
│   ├── service-screener/         # Service Screener 분석 결과
│   ├── security/                 # 보안 점검 결과
│   ├── well-architected/         # Well-Architected 리뷰 결과
│   └── architecture/             # 아키텍처 다이어그램 결과
├── requirements.txt              # Python 의존성
├── run_archiq.sh                # 🚀 메인 실행 스크립트
├── run_service_screener.sh      # Service Screener 실행 스크립트
├── run_security_check.sh        # 보안 점검 실행 스크립트
├── run_well_architected.sh      # Well-Architected 리뷰 실행 스크립트
├── run_architecture_diagram.sh  # 아키텍처 다이어그램 실행 스크립트
└── LICENSE                      # MIT 라이선스
```

## 🛠️ 설치 및 설정

### 1. 저장소 복제
```bash
git clone <repository-url>
cd archiQ
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

**주요 의존성:**
- `pytest==7.0.1` - 테스트 프레임워크
- `pytest-mock==3.10.0` - 모킹 라이브러리
- `websockets==10.1` - WebSocket 통신
- `inquirer==3.1.3` - 대화형 CLI 인터페이스
- `boto3>=1.26.0` - AWS SDK
- `botocore>=1.29.0` - AWS 핵심 라이브러리

### 3. Amazon Q Developer CLI 설정
```bash
# AWS 자격 증명 설정
aws configure
# 또는 환경 변수 설정
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=ap-northeast-2
```

### 4. 실행 권한 설정
```bash
chmod +x *.sh
```

## 🚀 사용 방법

### 기본 실행
```bash
# 메인 ArchiQ 실행
./run.sh

# 또는 Python으로 직접 실행
python src/cli.py
```

### 개별 기능 실행
```bash
# Service Screener 결과 기반 Well-Architected Review
./run_service_screener.sh

# AWS 리소스 기반 보안 점검
./run_security_check.sh

# AWS 리소스 기반 Well-Architected 리뷰
./run_well_architected.sh

# AWS 리소스 기반 아키텍처 다이어그램 생성
./run_architecture_diagram.sh
```

### CLI 메뉴 옵션
```
ArchiQ - AWS 아키텍처 리뷰 도구를 선택하세요:
  1. Service Screener 결과 기반 Well-Architected Review
  2. AWS 리소스 기반 보안 점검  
  3. AWS 리소스 기반 Well-Architected 리뷰
  4. AWS 리소스 기반 아키텍처 다이어그램 생성
  5. 종료
```

## 📊 생성되는 보고서

모든 분석 결과는 `output/` 디렉토리에 HTML 형식으로 저장됩니다:

### 보고서 특징
- **종합 요약 대시보드**: 핵심 지표 및 개선 기회
- **시각적 다이어그램**: Mermaid를 사용한 아키텍처 표현
- **상세 분석**: 각 AWS 서비스별 현재 상태 및 권장사항
- **실행 계획**: 구체적인 AWS CLI 명령어 및 구현 방법
- **우선순위별 권장사항**: High/Medium/Low 분류된 개선 방안

### 디자인 특징
- **푸른색 테마**: 전문적이고 신뢰감 있는 디자인
- **반응형 레이아웃**: 다양한 화면 크기 지원
- **일관된 브랜딩**: 모든 보고서에서 동일한 디자인 언어 사용

## 🔧 고급 사용법

### 프롬프트 커스터마이징
`src/prompt/` 디렉토리의 Markdown 파일을 수정하여 분석 기준을 조정할 수 있습니다:

- `service_screener_review.md`: Service Screener 분석 프롬프트
- `security_check.md`: 보안 점검 프롬프트  
- `well_architected_review.md`: Well-Architected 리뷰 프롬프트
- `architecture_diagram.md`: 아키텍처 다이어그램 생성 프롬프트

### 리전 설정
기본 리전은 서울(ap-northeast-2)로 설정되어 있으며, 각 기능 실행 시 다른 리전을 선택할 수 있습니다.

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🆘 지원

문제가 발생하거나 질문이 있으시면:
- GitHub Issues에 문제를 등록해주세요
- 프로젝트 Wiki를 확인해주세요
- 커뮤니티 토론에 참여해주세요

## 🔄 버전 히스토리

### v2.1.0 (Latest)
- ✅ 코드 간소화 및 안정성 개선
- ✅ 복잡한 예외 처리 제거
- ✅ `communicate()` 방식으로 안정성 확보
- ✅ Hanging 문제 완전 해결

### v2.0.0
- ✅ Interactive Session 기반 안정성 개선
- ✅ 자동 프롬프트 응답 시스템
- ✅ HTML 보고서 디자인 표준화

### v1.0.0
- ✅ 기본 AWS 아키텍처 분석 기능
- ✅ Service Screener 통합
- ✅ Well-Architected Framework 지원

---

**ArchiQ**로 AWS 아키텍처를 더 안전하고 효율적으로 만들어보세요! 🚀
