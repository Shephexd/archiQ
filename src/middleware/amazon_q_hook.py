import subprocess
import sys
import os
import time
import tempfile
import threading
import queue
from typing import Dict, Any, Optional
import re
import itertools


class SpinnerManager:
    """
    Spinner manager for showing progress during thinking
    """
    
    def __init__(self):
        self.spinner_chars = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.is_spinning = False
        self.spinner_thread = None
        self.current_message = ""
    
    def start(self, message="🤔 Thinking"):
        """Start spinner with message"""
        if self.is_spinning:
            return
            
        self.current_message = message
        self.is_spinning = True
        self.spinner_thread = threading.Thread(target=self._spin, daemon=True)
        self.spinner_thread.start()
    
    def stop(self):
        """Stop spinner"""
        if not self.is_spinning:
            return
            
        self.is_spinning = False
        if self.spinner_thread:
            self.spinner_thread.join(timeout=1)
        
        # Clear the spinner line
        print(f"\r{' ' * (len(self.current_message) + 10)}\r", end='', flush=True)
    
    def _spin(self):
        """Spinner animation loop"""
        while self.is_spinning:
            spinner_char = next(self.spinner_chars)
            print(f"\r{spinner_char} {self.current_message}...", end='', flush=True)
            time.sleep(0.1)


class QChatInteractiveSession:
    """
    Interactive qchat session handler with real-time output and spinner
    """
    
    def __init__(self):
        self.process = None
        self.is_active = False
        self.output_queue = queue.Queue()
        self.reader_thread = None
        self.spinner = SpinnerManager()
        
    def start_session(self):
        """Start the interactive qchat session"""
        try:
            self.process = subprocess.Popen(
                ["qchat", "chat", "--trust-all-tools"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr to stdout
                text=True,
                universal_newlines=True,
                bufsize=0  # Unbuffered
            )
            self.is_active = True
            print("[INFO] 🚀 Interactive qchat session started")
            
            # Start output reader thread
            self.reader_thread = threading.Thread(target=self._read_output, daemon=True)
            self.reader_thread.start()
            
            # Wait for initialization
            time.sleep(5)
            return True
            
        except Exception as e:
            print(f"[ERROR] ❌ Failed to start qchat session: {e}")
            return False
    
    def _read_output(self):
        """Read output from process in separate thread"""
        try:
            while self.is_active and self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    self.output_queue.put(line.rstrip('\n\r'))
                else:
                    time.sleep(0.1)
        except Exception as e:
            print(f"[WARNING] Output reader error: {e}")
    
    def _clean_line(self, line):
        """Clean ANSI escape sequences and spinner characters"""
        # Remove ANSI escape sequences
        # line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        # line = re.sub(r'\x1b\[[0-9]*[A-Za-z]', '', line)
        # Remove spinner characters
        line = re.sub(r'[⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏]', '', line)
        return line.strip()
    
    def _is_system_message(self, line):
        """Check if line is a system message to filter out"""
        system_patterns = [
            r'✓.*initialized',
            r'⚠.*warning',
            r'Did you know\?',
            r'/help',
            r'You are chatting with',
            r'To exit the CLI',
            r'ctrl-c to start chatting',
        ]
        
        for pattern in system_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
    
    def _is_thinking_message(self, line):
        """Check if line is a thinking message"""
        thinking_patterns = [
            r'^Thinking\.\.\.$',
            r'^Thinking\s*$',
            r'^\s*Thinking\s*\.\.\.\s*$',
            r'^\s*🤔\s*Thinking\s*$'
        ]
        
        for pattern in thinking_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
    
    def ask_question_interactive(self, question: str):
        """
        Ask question with real-time interactive output and spinner for thinking
        """
        if not self.is_active or not self.process:
            raise Exception("Session not active")
        
        print(f"[INFO] 💭 Processing question: {question[:200]}...")
        print("[INFO] 🔄 Sending question to Amazon Q...")
        
        try:
            # Send question
            self.process.stdin.write(question + '\n')
            self.process.stdin.flush()
            
            # Auto-respond to prompts
            auto_response_thread = threading.Thread(
                target=self._auto_respond_to_prompts, 
                daemon=True
            )
            auto_response_thread.start()
            
            # Read responses with timeout
            response_started = False
            no_output_count = 0
            max_no_output = 100  # 10 seconds of no output
            thinking_count = 0
            consecutive_thinking = 0
            
            while self.is_active:
                try:
                    line = self.output_queue.get(timeout=0.1)
                    no_output_count = 0
                    
                    cleaned_line = self._clean_line(line)
                    
                    # Skip empty lines and system messages
                    if not cleaned_line or self._is_system_message(cleaned_line):
                        continue
                    
                    # Handle thinking messages with spinner
                    if self._is_thinking_message(cleaned_line):
                        thinking_count += 1
                        consecutive_thinking += 1
                        
                        # Start spinner on first thinking message
                        if consecutive_thinking == 1:
                            self.spinner.start("🤔 Amazon Q is thinking")
                        
                        # Don't output the thinking message, let spinner handle it
                        continue
                    else:
                        # Stop spinner when we get actual content
                        if consecutive_thinking > 0:
                            self.spinner.stop()
                            consecutive_thinking = 0

                    # Detect start of actual response
                    if not response_started and len(cleaned_line) > 10:
                        response_started = True
                        print("[INFO] 📝 Receiving response...")

                    yield cleaned_line
                        
                except queue.Empty:
                    no_output_count += 1
                    if no_output_count > max_no_output:
                        # Stop spinner before finishing
                        self.spinner.stop()
                        print("[INFO] ⏰ No more output detected, finishing...")
                        break
                    continue
            
            # Ensure spinner is stopped
            self.spinner.stop()
                    
        except Exception as e:
            self.spinner.stop()
            print(f"[ERROR] ❌ Interactive question failed: {e}")
            raise e
    
    def _auto_respond_to_prompts(self):
        """Auto-respond to y/n/t prompts in separate thread"""
        try:
            while self.is_active and self.process and self.process.poll() is None:
                try:
                    line = self.output_queue.get(timeout=1.0)
                    
                    # Check for prompts that need auto-response
                    if any(prompt in line.lower() for prompt in ['(y/n)', '(y/n/t)', 'continue?', 'proceed?']):
                        print(f"[AUTO-RESPONSE] 🤖 Detected prompt: {line}")
                        print("[AUTO-RESPONSE] 🤖 Sending 'y' response...")
                        self.process.stdin.write('y\n')
                        self.process.stdin.flush()
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"[WARNING] Auto-response error: {e}")
                    break
                    
        except Exception as e:
            print(f"[WARNING] Auto-response thread error: {e}")
    
    def ask_question_with_file(self, question: str):
        """
        Use temporary file approach - more reliable than stdin
        """
        print(f"[INFO] Processing question: {question}")
        
        # Create temporary file with question
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(question + '\n')
            temp_file = f.name
        
        try:
            # Use file input instead of stdin
            cmd = ["qchat", "chat", "--trust-all-tools"]
            
            with open(temp_file, 'r') as input_file:
                result = subprocess.run(
                    cmd,
                    stdin=input_file,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            
            if result.stderr:
                print(f"[WARNING] stderr: {result.stderr}")
            
            # Process output line by line
            if result.stdout:
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line and not line.startswith('⠋') and not line.startswith('⠙'):  # Skip spinner characters
                        # Clean up ANSI escape sequences
                        import re
                        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                        clean_line = re.sub(r'\x1b\[[0-9]*[A-Za-z]', '', clean_line)
                        clean_line = clean_line.strip()
                        if clean_line and not clean_line.startswith('✓') and not clean_line.startswith('⚠'):
                            yield clean_line
            
            print("[INFO] Question processed successfully")
            
        except Exception as e:
            print(f"[ERROR] Failed to process question: {e}")
            raise e
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def ask_question_simple(self, question: str):
        """
        Simple method using echo and pipe - most reliable
        """
        print(f"[INFO] Processing question: {question}")
        
        try:
            # Use echo to pipe the question
            cmd = f'echo "{question}" | qchat chat --trust-all-tools'
            
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            
            if result.stderr:
                print(f"[WARNING] stderr: {result.stderr}")
            
            # Process output line by line
            if result.stdout:
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line:
                        # Clean up ANSI escape sequences and spinner characters
                        import re
                        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                        clean_line = re.sub(r'\x1b\[[0-9]*[A-Za-z]', '', clean_line)
                        # clean_line = re.sub(r'[⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏]', '', clean_line)
                        clean_line = clean_line.strip()
                        
                        # Filter out initialization messages and keep actual responses
                        if (clean_line and 
                            not clean_line.startswith('✓') and 
                            not clean_line.startswith('⚠') and
                            not 'mcp servers initialized' in clean_line and
                            not 'ctrl-c to start chatting' in clean_line and
                            not clean_line.startswith('Did you know?') and
                            not clean_line.startswith('/help') and
                            not clean_line.startswith('You are chatting with') and
                            not clean_line.startswith('To exit the CLI') and
                            len(clean_line) > 1):
                            yield clean_line
            
            print("[INFO] Question processed successfully")
            
        except Exception as e:
            print(f"[ERROR] Failed to process question: {e}")
            raise e
    
    def terminate_session(self):
        """Terminate the qchat session"""
        print("[INFO] 🛑 Terminating session...")
        
        # Stop spinner first
        self.spinner.stop()
        self.is_active = False
        
        if self.process:
            try:
                # Send quit command
                if self.process.poll() is None:
                    try:
                        self.process.stdin.write('/quit\n')
                        self.process.stdin.flush()
                        time.sleep(1)
                    except:
                        pass
                
                # Terminate process
                if self.process.poll() is None:
                    self.process.terminate()
                    self.process.wait(timeout=5)
                    
                print("[INFO] ✅ Interactive qchat session terminated")
            except Exception as e:
                print(f"[WARNING] ⚠️ Error during termination: {e}")
                try:
                    self.process.kill()
                except:
                    pass
            finally:
                self.process = None
        
        # Wait for reader thread to finish
        if self.reader_thread and self.reader_thread.is_alive():
            self.reader_thread.join(timeout=2)


class AmazonQDeveloperHook:
    """
    Enhanced Amazon Q Developer Hook with real-time interaction
    """

    def __init__(self, ide_extension: bool = False):
        self.ide_extension = ide_extension
        self.interactive_session = None

    def start_interactive_session_with_tools(self):
        """Start an interactive session with --trust-all-tools"""
        self.interactive_session = QChatInteractiveSession()
        return self.interactive_session.start_session()
    
    def ask_question_with_auto_responses(self, question: str):
        """
        Ask a question using interactive session with real-time output
        """
        if not self.interactive_session:
            print("[INFO] 🚀 Starting new interactive session...")
            if not self.start_interactive_session_with_tools():
                raise Exception("Failed to start interactive session")
        
        try:
            for line in self.interactive_session.ask_question_interactive(question):
                yield line
        except Exception as e:
            print(f"[ERROR] ❌ Interactive question failed: {e}")
            # Try to restart session once
            print("[INFO] 🔄 Attempting to restart session...")
            self.end_interactive_session_with_tools()
            if self.start_interactive_session_with_tools():
                for line in self.interactive_session.ask_question_interactive(question):
                    yield line
            else:
                raise e
    
    def ask_question_stream(self, question: str, callback=None):
        """
        Main streaming method used by CLI - enhanced with progress tracking
        """
        print("[INFO] 🎯 Processing question with real-time streaming")
        print(f"[INFO] 📝 Question preview: {question[:150]}...")
        
        try:
            line_count = 0
            start_time = time.time()
            
            for line in self.ask_question_with_auto_responses(question):
                line_count += 1
                elapsed_time = time.time() - start_time
                
                # Show progress every 100 lines
                if line_count % 100 == 0:
                    print(f"[PROGRESS] 📊 {line_count} lines processed in {elapsed_time:.1f}s")
                
                if callback:
                    callback(line)
                else:
                    yield line
                    
            total_time = time.time() - start_time
            print(f"[INFO] ✅ Stream completed! {line_count} lines in {total_time:.1f}s")
            
        except Exception as e:
            print(f"[ERROR] ❌ Stream error: {e}")
            raise e
    
    def ask_question_direct(self, question: str) -> Dict[Any, Any]:
        """
        Direct question method - returns all output at once
        """
        print("[INFO] 🎯 Processing direct question")
        
        try:
            response_lines = []
            for line in self.ask_question_with_auto_responses(question):
                response_lines.append(line)
            
            return {"raw_output": "\n".join(response_lines)}
            
        except Exception as e:
            raise Exception(f"Amazon Q Developer command failed: {str(e)}")
    
    def end_interactive_session_with_tools(self):
        """End the interactive session"""
        if self.interactive_session:
            self.interactive_session.terminate_session()
            self.interactive_session = None

    def __del__(self):
        """Cleanup when object is destroyed"""
        self.end_interactive_session_with_tools()


def main():
    """Simple test"""
    hook = AmazonQDeveloperHook()
    
    print("Amazon Q Developer Hook - Simplified Version")
    print("=" * 50)
    
    try:
        question = input("Enter your question: ").strip()
        if question:
            print("-" * 50)
            for line in hook.ask_question_stream(question):
                print(line)
            print("-" * 50)
            print("Test completed!")
    except KeyboardInterrupt:
        print("\nTest interrupted")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
