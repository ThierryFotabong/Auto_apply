import customtkinter as ctk
from automation import LinkedInBot
from ai_processor import tailor_resume_for_job
import threading
import traceback

class JobBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Job Application Bot")
        self.geometry("600x700")
        self.resizable(False, False)

        # LinkedIn Email
        self.label_email = ctk.CTkLabel(self, text="LinkedIn Email:")
        self.label_email.pack(pady=(20, 0), anchor="w", padx=20)
        self.entry_email = ctk.CTkEntry(self, width=400)
        self.entry_email.pack(pady=(0, 10), padx=20)

        # LinkedIn Password
        self.label_password = ctk.CTkLabel(self, text="LinkedIn Password:")
        self.label_password.pack(anchor="w", padx=20)
        self.entry_password = ctk.CTkEntry(self, width=400, show="*")
        self.entry_password.pack(pady=(0, 10), padx=20)

        # Job Keywords
        self.label_keywords = ctk.CTkLabel(self, text="Job Keywords (e.g., 'Software Engineer'):")
        self.label_keywords.pack(anchor="w", padx=20)
        self.entry_keywords = ctk.CTkEntry(self, width=400)
        self.entry_keywords.pack(pady=(0, 10), padx=20)

        # Location
        self.label_location = ctk.CTkLabel(self, text="Location (e.g., 'Belgium'):")
        self.label_location.pack(anchor="w", padx=20)
        self.entry_location = ctk.CTkEntry(self, width=400)
        self.entry_location.pack(pady=(0, 10), padx=20)

        # Base Resume
        self.label_resume = ctk.CTkLabel(self, text="Base Resume:")
        self.label_resume.pack(anchor="w", padx=20)
        self.text_resume = ctk.CTkTextbox(self, width=540, height=200)
        self.text_resume.pack(pady=(0, 20), padx=20)

        # Start Bot Button
        self.start_button = ctk.CTkButton(self, text="Start Bot", command=self.start_bot_thread)
        self.start_button.pack(pady=(0, 20))

        # Status Log
        self.label_status = ctk.CTkLabel(self, text="Status Log:")
        self.label_status.pack(anchor="w", padx=20)
        self.text_status = ctk.CTkTextbox(self, width=540, height=120)
        self.text_status.pack(pady=(0, 20), padx=20)
        self.text_status.configure(state="disabled")

    def start_bot_thread(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        keywords = self.entry_keywords.get()
        location = self.entry_location.get()
        base_resume = self.text_resume.get("1.0", "end").strip()
        self.log_status("[Thread] Starting bot thread...")
        thread = threading.Thread(target=self.run_bot_logic, args=(email, password, keywords, location, base_resume))
        thread.start()

    def run_bot_logic(self, email, password, keywords, location, base_resume):
        try:
            self.log_status("Logging in...")
            print("[DEBUG] Logging in...")
            bot = LinkedInBot(email, password)
            bot.login()
            self.log_status("Searching for jobs...")
            print("[DEBUG] Searching for jobs...")
            bot.search_jobs(keywords, location)
            self.log_status("Getting job descriptions...")
            print("[DEBUG] Getting job descriptions...")
            job_descriptions = bot.get_job_descriptions()
            for idx, job_desc in enumerate(job_descriptions, 1):
                self.log_status(f"Tailoring resume for job {idx}...")
                print(f"[DEBUG] Tailoring resume for job {idx}...")
                tailored_resume = tailor_resume_for_job(base_resume, job_desc)
                self.log_status(f"Tailored Resume for Job {idx}:\n{tailored_resume}\n{'-'*40}")
            self.log_status("Process finished.")
            print("[DEBUG] Process finished.")
        except Exception as e:
            tb = traceback.format_exc()
            self.log_status(f"Error: {str(e)}\n{tb}")
            print(f"[ERROR] {str(e)}\n{tb}")
        finally:
            try:
                bot.close()
            except Exception as e:
                self.log_status(f"Error closing bot: {str(e)}")
                print(f"[ERROR] Error closing bot: {str(e)}")

    def log_status(self, message):
        self.text_status.configure(state="normal")
        self.text_status.insert("end", message + "\n")
        self.text_status.see("end")
        self.text_status.configure(state="disabled")

if __name__ == "__main__":
    app = JobBotApp()
    app.mainloop()