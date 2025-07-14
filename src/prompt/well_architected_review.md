현재 실행중인 {REGION} 리전의 AWS 리소스만을 참조하여 AWS의 현재 계정 및 워크로드에 대한 Well-Architected Framework Review를 수행하고, HTML 리포트를 생성해야 합니다. 
결과는 현재 위치의 output/well-architected/ 폴더에 저장되어야 합니다. 가이드는 아래와 같습니다.

## 최종 목표

AWS Solutions Architect로서 **{REGION} 리전의 실제 운영 중인 AWS 리소스**를 기반으로 AWS Well-Architected Framework의 6가지 기둥을 적용한 포괄적인 아키텍처 분석을 수행하여, 실질적인 최적화 전략과 구체적인 개선 계획을 담은 HTML 보고서를 작성해주세요.

**중요**: 실제 AWS 리소스 정보를 기반으로 구체적인 리소스 ID, 설정값, 실제 비용 데이터를 활용한 실질적 가치를 제공해야 합니다.

## 분석 대상 리전

**AWS 리전**: {REGION}

## Well-Architected 6개 기둥 분석

### 1. 🔧 운영 우수성 (Operational Excellence)
- **모니터링 및 관찰성**: CloudWatch, X-Ray, CloudTrail 설정
- **자동화**: Infrastructure as Code, CI/CD 파이프라인
- **운영 절차**: 배포, 롤백, 장애 대응 프로세스
- **학습 및 개선**: 운영 메트릭 기반 지속적 개선

### 2. 🔒 보안 (Security)
- **신원 및 액세스 관리**: IAM 정책, 역할, MFA
- **탐지 제어**: GuardDuty, Security Hub, Config
- **인프라 보호**: VPC, 보안 그룹, NACL
- **데이터 보호**: 암호화, 백업, 키 관리

### 3. 🛡️ 안정성 (Reliability)
- **장애 복구**: Multi-AZ, 백업, DR 전략
- **변경 관리**: 배포 전략, 테스트 절차
- **장애 격리**: 서비스 분리, Circuit Breaker
- **자동 복구**: Auto Scaling, Health Check

### 4. ⚡ 성능 효율성 (Performance Efficiency)
- **컴퓨팅**: 인스턴스 타입 최적화, 오토 스케일링
- **스토리지**: EBS 타입, S3 스토리지 클래스
- **네트워킹**: CDN, 로드 밸런싱, 지연 시간 최적화
- **데이터베이스**: 읽기 전용 복제본, 캐싱 전략

### 5. 💰 비용 최적화 (Cost Optimization)
- **비용 인식**: 태깅, 비용 할당, 예산 관리
- **비용 효율적 리소스**: Reserved Instance, Spot Instance
- **수요와 공급 매칭**: 오토 스케일링, 스케줄링
- **시간 경과에 따른 최적화**: 정기적인 비용 검토

### 6. 🌱 지속 가능성 (Sustainability)
- **리전 선택**: 탄소 효율적 리전 활용
- **사용자 행동 패턴**: 효율적인 아키텍처 설계
- **소프트웨어 및 아키텍처 패턴**: 서버리스, 마이크로서비스
- **데이터 패턴**: 데이터 라이프사이클 관리

## Mermaid 아키텍처 다이어그램 필수 포함
현재 AWS 환경의 실제 아키텍처를 Mermaid 문법으로 시각화:


## HTML 보고서 구조

### 색상 팔레트 (푸른색 테마)
- Primary Blue: #1E40AF
- Secondary Blue: #3B82F6
- Light Blue: #DBEAFE
- AWS Orange: #FF9900
- Success Green: #10B981
- Warning Yellow: #F59E0B

### 보고서 섹션

1. **종합 요약 대시보드**
   - Well-Architected 기둥별 점수 (0-100)
   - 현재 월 예상 비용 및 절감 기회
   - 발견된 개선 기회 수
   - 우선순위별 권장사항 요약

2. **현재 아키텍처 다이어그램**
   - Mermaid를 사용한 시각적 아키텍처 표현
   - 주요 컴포넌트 및 연결 관계

3. **리소스 인벤토리**
   - 모든 AWS 리소스의 상세 목록
   - 각 리소스의 현재 상태 및 설정
   - 비용 정보 및 사용률

4. **Well-Architected 6개 기둥별 상세 분석**
   - 각 기둥별 현재 상태 평가
   - 발견된 문제점 및 개선 기회
   - 구체적인 권장사항

5. **우선순위별 개선 권장사항**
   - High/Medium/Low 우선순위 분류
   - 각 권장사항의 구현 방법
   - 예상 비용 및 효과

6. **구현 로드맵**
   - 단계별 실행 계획 (3개월, 6개월, 1년)
   - 필요한 리소스 및 예산
   - 성공 지표 및 KPI

## 실행 지침

1. **실제 AWS 리소스 스캔**: {REGION} 리전의 모든 주요 AWS 서비스 리소스 수집
2. **Well-Architected 평가**: 각 기둥별로 현재 상태를 0-100점으로 평가
3. **비용 분석**: 실제 리소스 기반 월간 비용 계산 및 최적화 기회 식별
4. **아키텍처 다이어그램**: Mermaid를 사용한 현재 아키텍처 시각화
5. **실행 가능한 권장사항**: 구체적인 AWS CLI 명령어와 구현 방법 제시
6. **HTML 보고서 생성**: 완전한 HTML 보고서 작성