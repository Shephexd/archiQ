#!/usr/bin/env python3
import inquirer
from middleware.amazon_q_hook import AmazonQDeveloperHook
import json
import sys
import os
import shutil
from datetime import datetime


class ArchiQCLI:
    def __init__(self):
        self.q_hook = AmazonQDeveloperHook()
        self.default_region = 'ap-northeast-2'  # Seoul region as default
        
        # Get terminal size for better formatting
        self.terminal_width = shutil.get_terminal_size().columns
        self.max_width = min(120, self.terminal_width - 4)  # Leave some margin

        # Load prompts for core functions only
        self.prompts = self._load_prompts()

    def _clear_screen(self):
        """Clear screen and reset cursor position"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def _print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * self.max_width)
        print(f"🚀 {title}".center(self.max_width))
        print("=" * self.max_width)
    
    def _print_separator(self, char="-"):
        """Print separator line"""
        print(char * self.max_width)
    
    def _wrap_text(self, text, width=None):
        """Wrap text to fit terminal width"""
        if width is None:
            width = self.max_width
        
        import textwrap
        return textwrap.fill(text, width=width)

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
        """Execute review and save results - enhanced with better formatting and progress tracking"""
        self._clear_screen()
        self._print_header(title)
        
        full_response = ""
        start_time = datetime.now()
        
        try:
            line_count = 0
            char_count = 0
            last_progress_time = start_time
            
            print(f"📡 Amazon Q Developer에 연결 중...")
            print(f"💭 질문 처리 중: {question[:100]}...")
            self._print_separator()
            
            # Buffer for collecting output
            output_buffer = []
            buffer_size = 50  # Lines to buffer before displaying
            
            for line in self.q_hook.ask_question_stream(question):
                current_time = datetime.now()
                elapsed = (current_time - start_time).total_seconds()
                
                # Clean and format the line
                clean_line = line.strip()
                if not clean_line:
                    continue
                
                # Wrap long lines to fit terminal
                wrapped_lines = self._wrap_text(clean_line).split('\n')
                
                for wrapped_line in wrapped_lines:
                    output_buffer.append(wrapped_line)
                    full_response += wrapped_line + "\n"
                    line_count += 1
                    char_count += len(wrapped_line)
                
                # Display buffer when it's full or show progress
                if len(output_buffer) >= buffer_size or (current_time - last_progress_time).total_seconds() > 30:
                    # Display buffered content
                    for buffered_line in output_buffer:
                        print(buffered_line)
                    output_buffer.clear()
                    
                    # Show progress
                    if (current_time - last_progress_time).total_seconds() > 30:
                        self._print_separator("·")
                        progress_msg = f"📊 진행상황: {line_count}줄 ({char_count:,}자) | 경과시간: {elapsed:.1f}초"
                        print(self._wrap_text(progress_msg))
                        self._print_separator("·")
                        last_progress_time = current_time
            
            # Display remaining buffer
            for buffered_line in output_buffer:
                print(buffered_line)
            
        except KeyboardInterrupt:
            print(f"\n⚠️ 사용자에 의해 중단되었습니다.")
            input("\n계속하려면 Enter를 누르세요...")
            return
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")
            print("🔄 잠시 후 다시 시도해주세요.")
            input("\n계속하려면 Enter를 누르세요...")
            return

        total_time = (datetime.now() - start_time).total_seconds()
        
        self._print_separator()
        completion_msg = f"✅ {title} 완료! | 총 {line_count}줄 ({char_count:,}자) | 소요시간: {total_time:.1f}초"
        print(self._wrap_text(completion_msg))
        self._print_separator()
        
        # Pause before returning to menu
        input("\n메뉴로 돌아가려면 Enter를 누르세요...")

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
            self._clear_screen()
            
            # Display welcome header
            print("\n" + "🏗️  ArchiQ - AWS 아키텍처 리뷰 도구".center(self.max_width))
            print("=" * self.max_width)
            print("AWS 아키텍처를 분석하고 개선 방안을 제시합니다".center(self.max_width))
            print("=" * self.max_width)
            
            questions = [
                inquirer.List('action',
                              message="원하는 기능을 선택하세요:",
                              choices=[
                                  ('1. Service Screener 결과 기반 Well-Architected Review', 'service_screener'),
                                  ('2. 사용중인 AWS 리소스 기반 보안 점검', 'security_check'),
                                  ('3. 사용중인 AWS 리소스 기반 Well-Architected 리뷰', 'well_architected'),
                                  ('4. 사용중인 AWS 리소스 기반 아키텍처 다이어그램 생성', 'architecture_diagram'),
                                  ('5. 종료', 'exit')
                              ])
            ]

            try:
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
                    self._clear_screen()
                    print("\n" + "감사합니다! 안녕히 가세요! 👋".center(self.max_width))
                    print("=" * self.max_width)
                    break
                    
            except KeyboardInterrupt:
                self._clear_screen()
                print("\n" + "프로그램을 종료합니다! 👋".center(self.max_width))
                break
            except Exception as e:
                print(f"\n❌ 메뉴 처리 중 오류 발생: {str(e)}")
                input("계속하려면 Enter를 누르세요...")
                continue


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