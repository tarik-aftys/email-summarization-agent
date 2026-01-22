import time
import os
from src.emailExtract import get_credentials, list_last_messages, save_emails_to_file
from src.agent import summarize_email, save_outputs

OUTPUTS_DIR = "outputs"
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def main():

    try:
        creds = get_credentials()
        emails = list_last_messages(creds.token)
        
        if not emails:
            return
        save_emails_to_file(emails, os.path.join(OUTPUTS_DIR, "emails.txt"))
        for i, email in enumerate(emails, 1):
            try:
                summary = summarize_email(email.get('body', 'No content available'))
                save_outputs(summary, OUTPUTS_DIR)
                
                if i < len(emails):
                    time.sleep(2)
                    
            except Exception as e:
                error_str = str(e)
                print(f"\nErreur lors du résumé de l'email {i}: {error_str}")
    except Exception as e:
        print(f"\nERREUR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
