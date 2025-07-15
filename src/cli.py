#!/usr/bin/env python3
import inquirer
from middleware.amazon_q_hook import AmazonQDeveloperHook
import json
import sys
import os
from datetime import datetime


class ArchiQCLI:
    def __init__(self):
        self.q_hook = AmazonQDeveloperHook()
        self.default_region = 'ap-northeast-2'  # Seoul region as default

        # Load prompts for core functions only
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Load core prompt templates"""
        prompts = {}
        prompt_files = {
            'service_screener_review': 'service_screener_review.md',
            'security_check': 'security_check.md',
            'well_architected_review': 'well_architected_review.md',
            'architecture_diagram': 'architecture_diagram.md'
        }

        for key, filename in prompt_files.items():
            try:
                with open(f'src/prompt/{filename}', 'r', encoding='utf-8') as f:
                    prompts[key] = f.read()
            except FileNotFoundError:
                print(f"Warning: Prompt file {filename} not found")
                prompts[key] = ""

        return prompts

    def service_screener_review(self):
        """Perform Well-Architected Review based on Service Screener Results"""
        questions = [
            inquirer.Path('directory',
                          message="Service Screener 결과가 있는 디렉토리 경로를 입력하세요:",
                          default=os.getcwd(),
                          path_type=inquirer.Path.DIRECTORY,
                          exists=True)
        ]
        answers = inquirer.prompt(questions)

        if answers:
            directory_path = answers['directory']
            print(f"\n{directory_path}의 Service Screener 결과를 기반으로 Well-Architected Review를 수행합니다...\n")

            # Construct question with prompt template
            question = self.prompts['service_screener_review'].replace("{DIR_PATH}", directory_path)

            self._execute_review(question, "Service Screener 기반 Well-Architected Review")

    def security_check_review(self):
        """Perform security check based on AWS resources"""
        region = self._get_region_input()

        print(f"\n{region} 리전의 AWS 리소스를 기반으로 보안 점검을 수행합니다...\n")

        # Construct question with prompt template
        question = self.prompts['security_check'].replace("{REGION}", region)

        self._execute_review(question, f"{region} 리전 보안 점검 보고서")

    def well_architected_review(self):
        """Perform Well-Architected review based on AWS resources"""
        region = self._get_region_input()

        print(f"\n{region} 리전의 AWS 리소스를 기반으로 Well-Architected 리뷰를 수행합니다...\n")

        # Construct question with prompt template
        question = self.prompts['well_architected_review'].replace("{REGION}", region)

        self._execute_review(question, f"{region} 리전 Well-Architected 리뷰 보고서")

    def architecture_diagram_review(self):
        """Generate architecture diagram using draw.io format"""
        region = self._get_region_input()

        print(f"\n{region} 리전의 AWS 리소스를 기반으로 아키텍처 다이어그램을 생성합니다...\n")

        # Construct question with prompt template
        question = self.prompts['architecture_diagram'].replace("{REGION}", region)
        self._execute_review(question, f"{region} 리전 아키텍처 다이어그램")

    def _get_region_input(self):
        """Get AWS region input from user"""
        questions = [
            inquirer.Text('region',
                          message=f"AWS 리전을 입력하세요 (기본값: {self.default_region}):",
                          default=self.default_region)
        ]
        answers = inquirer.prompt(questions)
        return answers['region'] if answers else self.default_region

    def _execute_review(self, question, title):
        """Execute review and save results - enhanced with spinner and progress tracking"""
        print(f"\n🚀 {title} 생성을 시작합니다...")
        print("=" * 80)

        full_response = ""
        start_time = datetime.now()

        try:
            line_count = 0
            last_progress_time = start_time
            thinking_detected = False

            print("📡 Amazon Q Developer에 연결 중...")

            for line in self.q_hook.ask_question_stream(question):
                current_time = datetime.now()
                elapsed = (current_time - start_time).total_seconds()

                # Check if this looks like a thinking phase is over
                if not thinking_detected and line_count == 0 and len(line.strip()) > 20:
                    print("✨ 분석 완료! 응답을 생성하고 있습니다...")
                    thinking_detected = True

                # Print the actual response line
                print(line, flush=True)
                full_response += line + "\n"
                line_count += 1

                # Show progress every 30 seconds or 100 lines
                if (current_time - last_progress_time).total_seconds() > 60 or line_count % 100 == 0:
                    print(f"\n📊 [진행상황] {line_count}줄 처리됨 | 경과시간: {elapsed:.1f}초")
                    print("-" * 40)
                    last_progress_time = current_time

        except KeyboardInterrupt:
            print(f"\n⚠️ 사용자에 의해 중단되었습니다.")
            return
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")
            print("🔄 잠시 후 다시 시도해주세요.")
            return

        total_time = (datetime.now() - start_time).total_seconds()
        print("=" * 80)
        print(f"✅ {title} 완료!")
        print(f"📊 총 {line_count}줄 처리 | 소요시간: {total_time:.1f}초")

        # Save to file if response is substantial
        print(full_response.strip())

    def _get_filename(self, title):
        """Generate filename from title"""
        # Remove special characters and replace spaces with underscores
        import re
        filename = re.sub(r'[^\w\s-]', '', title)
        filename = re.sub(r'[-\s]+', '_', filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{filename}_{timestamp}.html"

    def main_menu(self):
        """Display the main menu and handle user input"""
        while True:
            questions = [
                inquirer.List('action',
                              message="ArchiQ - AWS 아키텍처 리뷰 도구를 선택하세요:",
                              choices=[
                                  ('1. Service Screener 결과 기반 Well-Architected Review', 'service_screener'),
                                  ('2. 사용중인 AWS 리소스 기반 보안 점검', 'security_check'),
                                  ('3. 사용중인 AWS 리소스 기반 Well-Architected 리뷰', 'well_architected'),
                                  ('4. 사용중인 AWS 리소스 기반 아키텍처 다이어그램 생성', 'architecture_diagram'),
                                  ('5. 종료', 'exit')
                              ])
            ]

            answers = inquirer.prompt(questions)

            if not answers:
                break

            if answers['action'] == 'service_screener':
                self.service_screener_review()
            elif answers['action'] == 'security_check':
                self.security_check_review()
            elif answers['action'] == 'well_architected':
                self.well_architected_review()
            elif answers['action'] == 'architecture_diagram':
                self.architecture_diagram_review()
            elif answers['action'] == 'exit':
                print("\n안녕히 가세요!")
                break


def main():
    cli = ArchiQCLI()
    try:
        cli.main_menu()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다!")
        sys.exit(0)
    except Exception as e:
        print(f"\n오류가 발생했습니다: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()