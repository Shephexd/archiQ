#!/bin/bash

# ArchiQ - AWS 리소스 기반 아키텍처 다이어그램 생성
# 사용법: ./run_architecture_diagram.sh [-r region]

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 기본 설정
DEFAULT_REGION="ap-northeast-2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="${SCRIPT_DIR}/src/prompt/architecture_diagram.md"
OUTPUT_DIR="${SCRIPT_DIR}/output/architecture"

# 출력 디렉토리 생성
mkdir -p "$OUTPUT_DIR"

# 도움말 함수
show_help() {
    echo -e "${BLUE}ArchiQ - AWS 리소스 기반 아키텍처 다이어그램 생성${NC}"
    echo ""
    echo "사용법: $0 [옵션]"
    echo ""
    echo "옵션:"
    echo "  -r, --region REGION    AWS 리전 설정 (기본값: ap-northeast-2)"
    echo "  -h, --help            이 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0                     # 기본 리전(ap-northeast-2) 사용"
    echo "  $0 -r us-east-1        # 특정 리전 지정"
    echo "  $0 --region eu-west-1  # 특정 리전 지정"
}

# 메인 함수
main() {
    local region="$DEFAULT_REGION"
    
    # 인수 파싱
    while [[ $# -gt 0 ]]; do
        case $1 in
            -r|--region)
                region="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 알 수 없는 옵션: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 프롬프트 파일 존재 확인
    if [ ! -f "$PROMPT_FILE" ]; then
        echo -e "${RED}❌ 프롬프트 파일이 존재하지 않습니다: $PROMPT_FILE${NC}"
        exit 1
    fi
    
    # AWS CLI 설치 확인
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI가 설치되지 않았습니다.${NC}"
        echo "AWS CLI를 설치하고 자격 증명을 설정해주세요."
        exit 1
    fi
    
    # Amazon Q CLI 설치 확인
    if ! command -v q &> /dev/null; then
        echo -e "${RED}❌ Amazon Q CLI가 설치되지 않았습니다.${NC}"
        echo "Amazon Q CLI를 설치해주세요."
        exit 1
    fi
    
    # AWS 자격 증명 확인
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}❌ AWS 자격 증명이 설정되지 않았습니다.${NC}"
        echo "aws configure 명령어로 자격 증명을 설정해주세요."
        exit 1
    fi
    
    echo -e "${GREEN}🌏 사용할 AWS 리전: $region${NC}"
    echo -e "${YELLOW}📊 AWS 리소스 기반 아키텍처 다이어그램 생성 실행 중...${NC}"
    echo ""
    
    # 프롬프트 내용 생성 (리전 치환)
    local prompt_content
    prompt_content=$(sed "s/{REGION}/$region/g" "$PROMPT_FILE")
    
    # Amazon Q CLI에 프롬프트 전달
    echo "$prompt_content" | q chat --trust-all-tools
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ AWS 리소스 기반 아키텍처 다이어그램 생성 완료!${NC}"
        echo -e "${BLUE}📊 결과는 output/architecture/ 디렉토리에서 확인하세요.${NC}"
    else
        echo -e "${RED}❌ 실행 중 오류가 발생했습니다.${NC}"
        exit 1
    fi
}

# 스크립트 실행
main "$@"
