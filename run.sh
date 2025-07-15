#!/bin/bash

# ArchiQ - AWS 아키텍처 리뷰 도구 실행 스크립트
# 사용법: ./run_archiq.sh [1|2|3|4] [추가옵션]

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 기본 설정
DEFAULT_REGION="ap-northeast-2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_DIR="${SCRIPT_DIR}/src/prompt"
OUTPUT_DIR="${SCRIPT_DIR}/output"

# 출력 디렉토리 생성
mkdir -p "${OUTPUT_DIR}"/{service-screener,security,well-architected,architecture}

# 도움말 함수
show_help() {
    echo -e "${BLUE}ArchiQ - AWS 아키텍처 리뷰 도구${NC}"
    echo ""
    echo "사용법: $0 [옵션] [기능번호]"
    echo ""
    echo "기능:"
    echo "  1    Service Screener 결과 기반 Well-Architected Review"
    echo "  2    AWS 리소스 기반 보안 점검"
    echo "  3    AWS 리소스 기반 Well-Architected 리뷰"
    echo "  4    AWS 리소스 기반 아키텍처 다이어그램 생성"
    echo ""
    echo "옵션:"
    echo "  -r, --region REGION    AWS 리전 설정 (기본값: ap-northeast-2)"
    echo "  -d, --dir PATH         Service Screener 결과 디렉토리 (기능 1용)"
    echo "  -h, --help            이 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0 1 -d /path/to/service-screener-results"
    echo "  $0 2 -r us-east-1"
    echo "  $0 3"
    echo "  $0 4 -r eu-west-1"
}

# 프롬프트 실행 함수
execute_prompt() {
    local prompt_content="$1"
    local feature_name="$2"
    
    echo -e "${YELLOW}🚀 ${feature_name} 실행 중...${NC}"
    echo -e "${BLUE}Amazon Q에 프롬프트를 전달합니다.${NC}"
    echo ""
    
    # Amazon Q CLI에 프롬프트 전달
    echo "$prompt_content" | q chat --trust-all-tools
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ ${feature_name} 완료!${NC}"
        echo -e "${BLUE}결과는 output/ 디렉토리에서 확인하세요.${NC}"
    else
        echo -e "${RED}❌ ${feature_name} 실행 중 오류가 발생했습니다.${NC}"
        exit 1
    fi
}

# Service Screener Review 실행
run_service_screener_review() {
    local dir_path="$1"
    
    if [ -z "$dir_path" ]; then
        echo -e "${RED}❌ Service Screener 결과 디렉토리를 지정해주세요.${NC}"
        echo "사용법: $0 1 -d /path/to/service-screener-results"
        exit 1
    fi
    
    if [ ! -d "$dir_path" ]; then
        echo -e "${RED}❌ 지정된 디렉토리가 존재하지 않습니다: $dir_path${NC}"
        exit 1
    fi
    
    local prompt_content
    prompt_content=$(awk -v dir_path="$dir_path" '{gsub(/{DIR_PATH}/, dir_path); print}' "$PROMPT_DIR/service_screener_review.md")
    
    execute_prompt "$prompt_content" "Service Screener 결과 기반 Well-Architected Review"
}

# 보안 점검 실행
run_security_check() {
    local region="$1"
    
    local prompt_content
    prompt_content=$(sed "s/{REGION}/$region/g" "$PROMPT_DIR/security_check.md")
    
    execute_prompt "$prompt_content" "AWS 리소스 기반 보안 점검"
}

# Well-Architected Review 실행
run_well_architected_review() {
    local region="$1"
    
    local prompt_content
    prompt_content=$(sed "s/{REGION}/$region/g" "$PROMPT_DIR/well_architected_review.md")
    
    execute_prompt "$prompt_content" "AWS 리소스 기반 Well-Architected 리뷰"
}

# 아키텍처 다이어그램 생성 실행
run_architecture_diagram() {
    local region="$1"
    
    local prompt_content
    prompt_content=$(sed "s/{REGION}/$region/g" "$PROMPT_DIR/architecture_diagram.md")
    
    execute_prompt "$prompt_content" "AWS 리소스 기반 아키텍처 다이어그램 생성"
}

# 메인 함수
main() {
    local region="$DEFAULT_REGION"
    local dir_path=""
    local function_num=""
    
    # 인수 파싱
    while [[ $# -gt 0 ]]; do
        case $1 in
            -r|--region)
                region="$2"
                shift 2
                ;;
            -d|--dir)
                dir_path="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            [1-4])
                function_num="$1"
                shift
                ;;
            *)
                echo -e "${RED}❌ 알 수 없는 옵션: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 기능 번호가 지정되지 않은 경우 메뉴 표시
    if [ -z "$function_num" ]; then
        echo -e "${BLUE}ArchiQ - AWS 아키텍처 리뷰 도구를 선택하세요:${NC}"
        echo "  1. Service Screener 결과 기반 Well-Architected Review"
        echo "  2. AWS 리소스 기반 보안 점검"
        echo "  3. AWS 리소스 기반 Well-Architected 리뷰"
        echo "  4. AWS 리소스 기반 아키텍처 다이어그램 생성"
        echo "  5. 종료"
        echo ""
        read -p "선택하세요 (1-5): " function_num
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
    
    # 프롬프트 파일 존재 확인
    if [ ! -d "$PROMPT_DIR" ]; then
        echo -e "${RED}❌ 프롬프트 디렉토리가 존재하지 않습니다: $PROMPT_DIR${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}🌏 사용할 AWS 리전: $region${NC}"
    echo ""
    
    # 기능 실행
    case $function_num in
        1)
            run_service_screener_review "$dir_path"
            ;;
        2)
            run_security_check "$region"
            ;;
        3)
            run_well_architected_review "$region"
            ;;
        4)
            run_architecture_diagram "$region"
            ;;
        5)
            echo -e "${BLUE}👋 ArchiQ를 종료합니다.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 잘못된 선택입니다. 1-5 사이의 숫자를 입력해주세요.${NC}"
            exit 1
            ;;
    esac
}

# 스크립트 실행
main "$@"