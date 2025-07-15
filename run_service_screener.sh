#!/bin/bash

# ArchiQ - Service Screener 결과 기반 Well-Architected Review
# 사용법: ./run_service_screener.sh -d /path/to/service-screener-results

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 기본 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="${SCRIPT_DIR}/src/prompt/service_screener_review.md"
OUTPUT_DIR="${SCRIPT_DIR}/output/service-screener"

# 출력 디렉토리 생성
mkdir -p "$OUTPUT_DIR"

# 도움말 함수
show_help() {
    echo -e "${BLUE}ArchiQ - Service Screener 결과 기반 Well-Architected Review${NC}"
    echo ""
    echo "사용법: $0 -d DIRECTORY"
    echo ""
    echo "옵션:"
    echo "  -d, --dir DIRECTORY    Service Screener 결과 디렉토리 (필수)"
    echo "  -h, --help            이 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0 -d /path/to/service-screener-results"
    echo "  $0 --dir ./screener-output"
}

# 메인 함수
main() {
    local dir_path=""
    
    # 인수 파싱
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--dir)
                dir_path="$2"
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
    
    # 필수 인수 확인
    if [ -z "$dir_path" ]; then
        echo -e "${RED}❌ Service Screener 결과 디렉토리를 지정해주세요.${NC}"
        show_help
        exit 1
    fi
    
    # 디렉토리 존재 확인
    if [ ! -d "$dir_path" ]; then
        echo -e "${RED}❌ 지정된 디렉토리가 존재하지 않습니다: $dir_path${NC}"
        exit 1
    fi
    
    # 프롬프트 파일 존재 확인
    if [ ! -f "$PROMPT_FILE" ]; then
        echo -e "${RED}❌ 프롬프트 파일이 존재하지 않습니다: $PROMPT_FILE${NC}"
        exit 1
    fi
    
    # Amazon Q CLI 설치 확인
    if ! command -v q &> /dev/null; then
        echo -e "${RED}❌ Amazon Q CLI가 설치되지 않았습니다.${NC}"
        echo "Amazon Q CLI를 설치해주세요."
        exit 1
    fi
    
    echo -e "${GREEN}📁 Service Screener 결과 디렉토리: $dir_path${NC}"
    echo -e "${YELLOW}🚀 Service Screener 결과 기반 Well-Architected Review 실행 중...${NC}"
    echo ""
    
    # 프롬프트 내용 생성 (디렉토리 경로 치환)
    local prompt_content
    prompt_content=$(awk -v dir_path="$dir_path" '{gsub(/{DIR_PATH}/, dir_path); print}' "$PROMPT_FILE")
    
    # Amazon Q CLI에 프롬프트 전달
    echo "$prompt_content" | q chat --trust-all-tools
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Service Screener 결과 기반 Well-Architected Review 완료!${NC}"
        echo -e "${BLUE}📊 결과는 output/service-screener/ 디렉토리에서 확인하세요.${NC}"
    else
        echo -e "${RED}❌ 실행 중 오류가 발생했습니다.${NC}"
        exit 1
    fi
}

# 스크립트 실행
main "$@"
