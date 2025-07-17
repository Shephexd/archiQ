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
        self.language = 'ko'  # Default language
        
        # Get terminal size for better formatting
        self.terminal_width = shutil.get_terminal_size().columns
        self.max_width = min(120, self.terminal_width - 4)  # Leave some margin

        # Language-specific texts
        self.texts = {
            'ko': {
                'title': '🏗️  ArchiQ - AWS 아키텍처 리뷰 도구',
                'subtitle': 'AWS 아키텍처를 분석하고 개선 방안을 제시합니다',
                'language_select': '언어를 선택하세요 (Select Language):',
                'menu_select': '원하는 기능을 선택하세요:',
                'menu_options': [
                    ('1. 사용중인 AWS 리소스 기반 현대화 경로 분석', 'modernization_path'),
                    ('2. 사용중인 AWS 리소스 기반 보안 점검', 'security_check'),
                    ('3. 사용중인 AWS 리소스 기반 Well-Architected 리뷰', 'well_architected'),
                    ('4. 사용중인 AWS 리소스 기반 아키텍처 다이어그램 생성', 'architecture_diagram'),
                    ('5. Service Screener 결과 기반 Well-Architected Review', 'service_screener'),
                    ('6. 종료', 'exit')
                ],
                'region_input': 'AWS 리전을 입력하세요 (기본값: {}):',
                'directory_input': 'Service Screener 결과가 있는 디렉토리 경로를 입력하세요:',
                'processing': '{} 리전의 AWS 리소스를 기반으로 {}을(를) 수행합니다...',
                'goodbye': '감사합니다! 안녕히 가세요! 👋',
                'exit_msg': '프로그램을 종료합니다! 👋',
                'continue_msg': '계속하려면 Enter를 누르세요...',
                'menu_return': '메뉴로 돌아가려면 Enter를 누르세요...',
                'error': '오류 발생: {}',
                'interrupted': '사용자에 의해 중단되었습니다.',
                'connecting': 'Amazon Q Developer에 연결 중...',
                'processing_question': '질문 처리 중: {}...',
                'progress': '진행상황: {}줄 ({}자) | 경과시간: {:.1f}초',
                'completed': '{} 완료! | 총 {}줄 ({}자) | 소요시간: {:.1f}초'
            },
            'en': {
                'title': '🏗️  ArchiQ - AWS Architecture Review Tool',
                'subtitle': 'Analyze AWS architecture and provide improvement recommendations',
                'language_select': '언어를 선택하세요 (Select Language):',
                'menu_select': 'Please select the desired function:',
                'menu_options': [
                    ('1. AWS Resource-based Modernization Path Analysis', 'modernization_path'),
                    ('2. AWS Resource-based Security Assessment', 'security_check'),
                    ('3. AWS Resource-based Well-Architected Review', 'well_architected'),
                    ('4. AWS Resource-based Architecture Diagram Generation', 'architecture_diagram'),
                    ('5. Service Screener Results-based Well-Architected Review', 'service_screener'),
                    ('6. Exit', 'exit')
                ],
                'region_input': 'Enter AWS region (default: {}):',
                'directory_input': 'Enter the directory path containing Service Screener results:',
                'processing': 'Performing {} based on AWS resources in {} region...',
                'goodbye': 'Thank you! Goodbye! 👋',
                'exit_msg': 'Exiting program! 👋',
                'continue_msg': 'Press Enter to continue...',
                'menu_return': 'Press Enter to return to menu...',
                'error': 'Error occurred: {}',
                'interrupted': 'Interrupted by user.',
                'connecting': 'Connecting to Amazon Q Developer...',
                'processing_question': 'Processing question: {}...',
                'progress': 'Progress: {} lines ({} chars) | Elapsed: {:.1f}s',
                'completed': '{} completed! | Total {} lines ({} chars) | Duration: {:.1f}s'
            }
        }

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
        """Load core prompt templates based on selected language"""
        prompts = {}
        prompt_files = {
            'modernization_path': 'modernization_path.md',
            'service_screener_review': 'service_screener_review.md',
            'security_check': 'security_check.md',
            'well_architected_review': 'well_architected_review.md',
            'architecture_diagram': 'architecture_diagram.md'
        }

        # Determine prompt directory based on language
        prompt_dir = f'src/prompt/{self.language}' if self.language == 'en' else 'src/prompt'

        for key, filename in prompt_files.items():
            try:
                with open(f'{prompt_dir}/{filename}', 'r', encoding='utf-8') as f:
                    prompts[key] = f.read()
            except FileNotFoundError:
                # Fallback to Korean version if English not found
                try:
                    with open(f'src/prompt/{filename}', 'r', encoding='utf-8') as f:
                        prompts[key] = f.read()
                except FileNotFoundError:
                    print(f"Warning: Prompt file {filename} not found")
                    prompts[key] = ""

        return prompts

    def _get_text(self, key):
        """Get localized text"""
        return self.texts[self.language].get(key, key)

    def _select_language(self):
        """Language selection menu"""
        questions = [
            inquirer.List('language',
                          message=self._get_text('language_select'),
                          choices=[
                              ('한국어 (Korean)', 'ko'),
                              ('English', 'en')
                          ])
        ]
        
        answers = inquirer.prompt(questions)
        if answers:
            self.language = answers['language']
            # Reload prompts with new language
            self.prompts = self._load_prompts()

    def modernization_path_review(self):
        """Perform modernization path analysis based on AWS resources"""
        region = self._get_region_input()

        analysis_type = "현대화 경로 분석" if self.language == 'ko' else "modernization path analysis"
        print(f"\n{self._get_text('processing').format(region, analysis_type)}\n")

        # Construct question with prompt template
        question = self.prompts['modernization_path'].replace("{REGION}", region)

        title = f"{region} 리전 현대화 경로 분석 보고서" if self.language == 'ko' else f"{region} Region Modernization Path Analysis Report"
        self._execute_review(question, title)

    def service_screener_review(self):
        """Perform Well-Architected Review based on Service Screener Results"""
        questions = [
            inquirer.Path('directory',
                          message=self._get_text('directory_input'),
                          default=os.getcwd(),
                          path_type=inquirer.Path.DIRECTORY,
                          exists=True)
        ]
        answers = inquirer.prompt(questions)

        if answers:
            directory_path = answers['directory']
            analysis_type = "Service Screener 기반 Well-Architected Review" if self.language == 'ko' else "Service Screener-based Well-Architected Review"
            print(f"\n{directory_path}의 Service Screener 결과를 기반으로 {analysis_type}를 수행합니다...\n")

            # Construct question with prompt template
            question = self.prompts['service_screener_review'].replace("{DIR_PATH}", directory_path)

            title = "Service Screener 기반 Well-Architected Review" if self.language == 'ko' else "Service Screener-based Well-Architected Review"
            self._execute_review(question, title)

    def security_check_review(self):
        """Perform security check based on AWS resources"""
        region = self._get_region_input()

        analysis_type = "보안 점검" if self.language == 'ko' else "security assessment"
        print(f"\n{self._get_text('processing').format(region, analysis_type)}\n")

        # Construct question with prompt template
        question = self.prompts['security_check'].replace("{REGION}", region)

        title = f"{region} 리전 보안 점검 보고서" if self.language == 'ko' else f"{region} Region Security Assessment Report"
        self._execute_review(question, title)

    def well_architected_review(self):
        """Perform Well-Architected review based on AWS resources"""
        region = self._get_region_input()

        analysis_type = "Well-Architected 리뷰" if self.language == 'ko' else "Well-Architected review"
        print(f"\n{self._get_text('processing').format(region, analysis_type)}\n")

        # Construct question with prompt template
        question = self.prompts['well_architected_review'].replace("{REGION}", region)

        title = f"{region} 리전 Well-Architected 리뷰 보고서" if self.language == 'ko' else f"{region} Region Well-Architected Review Report"
        self._execute_review(question, title)

    def architecture_diagram_review(self):
        """Generate architecture diagram using draw.io format"""
        region = self._get_region_input()

        analysis_type = "아키텍처 다이어그램 생성" if self.language == 'ko' else "architecture diagram generation"
        print(f"\n{self._get_text('processing').format(region, analysis_type)}\n")

        # Construct question with prompt template
        question = self.prompts['architecture_diagram'].replace("{REGION}", region)
        
        title = f"{region} 리전 아키텍처 다이어그램" if self.language == 'ko' else f"{region} Region Architecture Diagram"
        self._execute_review(question, title)

    def _get_region_input(self):
        """Get AWS region input from user"""
        questions = [
            inquirer.Text('region',
                          message=self._get_text('region_input').format(self.default_region),
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
            
            print(f"📡 {self._get_text('connecting')}")
            print(f"💭 {self._get_text('processing_question').format(question[:100])}")
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
                        progress_msg = f"📊 {self._get_text('progress').format(line_count, f'{char_count:,}', elapsed)}"
                        print(self._wrap_text(progress_msg))
                        self._print_separator("·")
                        last_progress_time = current_time
            
            # Display remaining buffer
            for buffered_line in output_buffer:
                print(buffered_line)
            
        except KeyboardInterrupt:
            print(f"\n⚠️ {self._get_text('interrupted')}")
            input(f"\n{self._get_text('continue_msg')}")
            return
        except Exception as e:
            print(f"\n❌ {self._get_text('error').format(str(e))}")
            retry_msg = "🔄 잠시 후 다시 시도해주세요." if self.language == 'ko' else "🔄 Please try again later."
            print(retry_msg)
            input(f"\n{self._get_text('continue_msg')}")
            return

        total_time = (datetime.now() - start_time).total_seconds()
        
        self._print_separator()
        completion_msg = f"✅ {self._get_text('completed').format(title, line_count, f'{char_count:,}', total_time)}"
        print(self._wrap_text(completion_msg))
        self._print_separator()
        
        # Pause before returning to menu
        input(f"\n{self._get_text('menu_return')}")

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
        # First, select language
        self._clear_screen()
        self._select_language()
        
        while True:
            self._clear_screen()
            
            # Display welcome header
            print(f"\n{self._get_text('title')}".center(self.max_width))
            print("=" * self.max_width)
            print(f"{self._get_text('subtitle')}".center(self.max_width))
            print("=" * self.max_width)
            
            # Show current language in menu
            lang_display = "한국어" if self.language == 'ko' else "English"
            print(f"Language: {lang_display}".center(self.max_width))
            print("-" * self.max_width)
            
            menu_options = self._get_text('menu_options').copy()
            # Add language change option
            lang_change_text = "언어 변경 (Change Language)" if self.language == 'ko' else "언어 변경 (Change Language)"
            menu_options.insert(-1, (f"7. {lang_change_text}", 'change_language'))
            
            questions = [
                inquirer.List('action',
                              message=self._get_text('menu_select'),
                              choices=menu_options)
            ]

            try:
                answers = inquirer.prompt(questions)
                
                if not answers:
                    break

                if answers['action'] == 'modernization_path':
                    self.modernization_path_review()
                elif answers['action'] == 'security_check':
                    self.security_check_review()
                elif answers['action'] == 'well_architected':
                    self.well_architected_review()
                elif answers['action'] == 'architecture_diagram':
                    self.architecture_diagram_review()
                elif answers['action'] == 'service_screener':
                    self.service_screener_review()
                elif answers['action'] == 'change_language':
                    self._select_language()
                elif answers['action'] == 'exit':
                    self._clear_screen()
                    print(f"\n{self._get_text('goodbye')}".center(self.max_width))
                    print("=" * self.max_width)
                    break
                    
            except KeyboardInterrupt:
                self._clear_screen()
                print(f"\n{self._get_text('exit_msg')}".center(self.max_width))
                break
            except Exception as e:
                error_msg = self._get_text('error').format(str(e))
                print(f"\n❌ {error_msg}")
                input(self._get_text('continue_msg'))
                continue


def main():
    cli = ArchiQCLI()
    try:
        cli.main_menu()
    except KeyboardInterrupt:
        exit_msg = "프로그램을 종료합니다!" if cli.language == 'ko' else "Exiting program!"
        print(f"\n{exit_msg}")
        sys.exit(0)
    except Exception as e:
        error_msg = f"오류가 발생했습니다: {str(e)}" if cli.language == 'ko' else f"An error occurred: {str(e)}"
        print(f"\n{error_msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()