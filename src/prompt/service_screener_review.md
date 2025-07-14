서비스 스크리너는 AWS의 정적 분석 스크립트로 현재 리소스가 모범사례에 따르는지에 대한 리포트를 제공합니다. 
{DIR_PATH} 경로의 결과 파일을 기반으로 Well-Architected Framework Review HTML 리포트를 생성하세요.
가이드는 아래와 같습니다.

## 최종 목표

AWS 전문 컨설턴트로서 **제공된 Service Screener 결과 파일**을 기반으로 포괄적인 Well-Architected Framework 분석을 수행하여, 구체적인 개선 계획과 실행 가능한 권장사항을 담은 HTML 보고서를 작성해주세요.

**중요**: 이 보고서는 실제 제공된 Service Screener 데이터를 기반으로 작성되어야 하며, 구체적인 리소스 ID, 설정값, 실제 발견된 문제점을 활용한 실질적 가치를 제공해야 합니다.

## 분석 대상 데이터

**디렉토리 경로**: {DIR_PATH}

## HTML 보고서 요구사항

### 색상 팔레트 (푸른색 테마)
- Primary Blue: #1E40AF
- Secondary Blue: #3B82F6  
- Light Blue: #DBEAFE
- AWS Orange: #FF9900
- Success Green: #10B981
- Warning Yellow: #F59E0B
- Danger Red: #EF4444

### 보고서 구조

1. **종합 요약 대시보드**
   - Service Screener 발견 이슈 수
   - 우선순위별 분류 (High/Medium/Low)
   - Well-Architected 기둥별 점수
   - 예상 개선 효과

2. **Service Screener 결과 분석**
   - 발견된 모든 이슈의 상세 분석
   - 각 이슈의 Well-Architected 기둥 매핑
   - 비즈니스 영향도 평가

3. **Well-Architected 6개 기둥별 분석**
   - 운영 우수성 (Operational Excellence)
   - 보안 (Security)
   - 안정성 (Reliability)
   - 성능 효율성 (Performance Efficiency)
   - 비용 최적화 (Cost Optimization)
   - 지속 가능성 (Sustainability)

4. **우선순위별 개선 권장사항**
   - 각 권장사항별 구현 방법
   - AWS CLI 명령어 예시
   - 예상 비용 및 효과

5. **구현 로드맵**
   - 단계별 실행 계획
   - 타임라인 및 리소스 요구사항
