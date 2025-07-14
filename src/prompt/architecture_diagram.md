현재 실행중인 {REGION} 리전의 AWS 리소스만을 참조하여 아키텍처 draw.io 포맷의 다이어그램을 생성합니다. 리포트 파일을 생성하거나 리소스를 조회하기 위한 추가적인 동의나 확인을 하지 않아도 됩니다.
결과는 현재 위치의 output/diagram/ 폴더에 저장되어야 합니다. 가이드는 아래와 같습니다.

# AWS 리소스 기반 아키텍처 다이어그램 생성 프롬프트

## 최종 목표

AWS Solutions Architect로서 **{REGION} 리전의 실제 운영 중인 AWS 리소스**를 기반으로 현재 아키텍처를 시각화하고, draw.io 호환 형식과 Mermaid 다이어그램을 포함한 포괄적인 아키텍처 문서를 생성하는 HTML 보고서를 작성해주세요.

**중요**: 실제 AWS 리소스 정보를 기반으로 정확한 아키텍처 다이어그램을 생성하고, 각 컴포넌트 간의 실제 연결 관계를 반영해야 합니다.

## 분석 대상 리전

**AWS 리전**: {REGION}

## 다이어그램 생성 요구사항

### 1. 현재 아키텍처 스캔
- VPC 및 네트워크 구성 요소
- 컴퓨팅 리소스 (EC2, Lambda, ECS 등)
- 데이터베이스 (RDS, DynamoDB, ElastiCache 등)
- 스토리지 (S3, EBS, EFS 등)
- 네트워킹 (ALB, NLB, CloudFront, API Gateway 등)
- 보안 (IAM, Security Groups, WAF 등)

### 2. 다이어그램 형식
- **draw.io XML**: draw.io에서 편집 가능한 형식
- **Mermaid 다이어그램**: 웹 브라우저에서 렌더링 가능한 형식
- **아키텍처 설명**: 각 컴포넌트의 역할과 연결 관계

### 3. 시각화 레벨
- **High-Level**: 전체 시스템 개요
- **Network-Level**: VPC, 서브넷, 보안 그룹 상세
- **Service-Level**: 개별 서비스 간 상호작용
