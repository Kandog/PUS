import os
import sys
import json
import logging
import shutil
import csv
from datetime import datetime

# Placeholder for Oracle database connection
# import oracledb

from config import CONFIG

def get_db_connection():
    """
    Establishes and returns a database connection.
    Replace with actual database connection details.
    """
    # Example for oracledb:
    # return oracledb.connect(user="your_user", password="your_password", dsn="your_dsn")
    logging.info("Connecting to the database (placeholder).")
    return None

def call_oracle_procedure(db_connection, category, file_name, payload):
    """
    Calls the Oracle PL/SQL procedure to insert data.
    """
    if db_connection is None:
        logging.info(f"Skipping Oracle procedure call for {file_name} (no DB connection).")
        # In a real scenario, you would raise an exception or handle this case.
        return True # Assume success for testing without a DB

    try:
        cursor = db_connection.cursor()
        cursor.callproc("INTERFACE_PAYMENTUS.PUS_PKG.RAW_DATA_ADD", [category, file_name, payload])
        cursor.close()
        logging.info(f"Successfully called RAW_DATA_ADD for {file_name}.")
        return True
    except Exception as e:
        logging.error(f"Error calling Oracle procedure for {file_name}: {e}")
        return False

def send_email(subject, body, recipients, attachment_path=None):
    """
    Placeholder function for sending an email.
    In a real implementation, this would use a library like smtplib.
    """
    logging.info(f"Sending email...")
    logging.info(f"  To: {', '.join(recipients)}")
    logging.info(f"  Subject: {subject}")
    logging.info(f"  Body: {body}")
    if attachment_path:
        logging.info(f"  Attachment: {attachment_path}")
    logging.info("Email sent (placeholder).")

def process_returns(cfg):
    """Processes return files."""
    returns_in_dir = cfg['returns_in']
    returns_out_dir = cfg['returns_out']
    archive_dir = cfg['archive_dir']
    os.makedirs(returns_in_dir, exist_ok=True)
    os.makedirs(returns_out_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)

    files = os.listdir(returns_in_dir)
    if not files:
        logging.info("No return files to process.")
        return

    for file_name in files:
        source_path = os.path.join(returns_in_dir, file_name)
        file_size = os.path.getsize(source_path)

        if file_size > 350:
            logging.info(f"File {file_name} is larger than 350 bytes. Emailing and archiving.")
            subject = f"Paymentus ({cfg['name']}) - Return"
            body = f"{cfg['name']} Return is attached."
            send_email(subject, body, cfg['return_emails'], source_path)

            # Copy to processed and then move to archive
            shutil.copy(source_path, os.path.join(returns_out_dir, file_name))
            shutil.move(source_path, os.path.join(archive_dir, file_name))
        else:
            logging.info(f"File {file_name} is smaller than 350 bytes. Archiving.")
            shutil.move(source_path, os.path.join(archive_dir, file_name))

        logging.info(f"Processed return file {file_name}.")

def csv_to_json(file_path):
    """Converts a CSV file to a JSON string."""
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
        return json.dumps(data, indent=4)
    except Exception as e:
        logging.error(f"Failed to convert {file_path} to JSON: {e}")
        return None

def process_postings(category, cfg):
    """Processes posting files."""
    posting_in_dir = cfg['posting_in']
    posting_out_dir = cfg['posting_out']
    in_dir = cfg['in_dir']
    received_dir = cfg['received_dir']

    os.makedirs(posting_in_dir, exist_ok=True)
    os.makedirs(posting_out_dir, exist_ok=True)
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(received_dir, exist_ok=True)

    # Move files from posting_in to in_dir
    for file_name in os.listdir(posting_in_dir):
        if not os.path.exists(os.path.join(posting_out_dir, file_name)):
            shutil.move(os.path.join(posting_in_dir, file_name), os.path.join(in_dir, file_name))
            logging.info(f"Moved {file_name} to working directory.")
            shutil.copy(os.path.join(in_dir, file_name), os.path.join(received_dir, file_name))
        else:
            logging.warning(f"File {file_name} already processed. Deleting duplicate from input.")
            os.remove(os.path.join(posting_in_dir, file_name))

    # Process files in in_dir
    files_to_process = os.listdir(in_dir)
    if not files_to_process:
        logging.info("No new posting files to process.")
        return

    db_connection = get_db_connection()
    for file_name in files_to_process:
        file_path = os.path.join(in_dir, file_name)
        logging.info(f"Processing posting file: {file_name}")

        json_payload = csv_to_json(file_path)

        if json_payload:
            if call_oracle_procedure(db_connection, category, file_name, json_payload):
                logging.info(f"Successfully processed {file_name}. Moving to processed directory.")
                shutil.move(file_path, os.path.join(posting_out_dir, file_name))
            else:
                logging.error(f"Failed to process {file_name}. It will remain in the 'in' directory for review.")

    if db_connection:
        db_connection.close()
        logging.info("Database connection closed.")

def process_deposits(cfg):
    """Processes deposit files."""
    deposit_in_dir = cfg['deposit_in']
    deposit_out_dir = cfg['deposit_out']
    os.makedirs(deposit_in_dir, exist_ok=True)
    os.makedirs(deposit_out_dir, exist_ok=True)

    files = [f for f in os.listdir(deposit_in_dir) if f.endswith('.csv')]
    if not files:
        logging.info("No deposit files to process.")
        return

    for file_name in files:
        source_path = os.path.join(deposit_in_dir, file_name)
        dest_path = os.path.join(deposit_out_dir, file_name)
        logging.info(f"Moving deposit file {source_path} to {dest_path}")
        shutil.move(source_path, dest_path)

def setup_logging(log_dir, category):
    """Sets up logging for the script."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'paymentus_{category}.log')

    # Rotate log file if it exists
    if os.path.exists(log_file):
        os.remove(log_file)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main(category):
    """Main processing function."""
    if category not in CONFIG:
        print(f"Error: Invalid category '{category}'. Must be one of {list(CONFIG.keys())}")
        sys.exit(1)

    cfg = CONFIG[category]
    setup_logging(cfg['log_dir'], category)

    logging.info(f"--- Starting processing for {cfg['name']} ---")

    process_deposits(cfg)
    process_returns(cfg)
    process_postings(category, cfg)

    logging.info(f"--- Finished processing for {cfg['name']} ---")

if __name__ == "__main__":
    # This script is intended to be run from the command line,
    # passing the category as an argument.
    # Example: python process_payments.py ambp
    if len(sys.argv) != 2:
        print("Usage: python process_payments.py <category>")
        print(f"Available categories: {', '.join(CONFIG.keys())}")
        sys.exit(1)

    category_arg = sys.argv[1].lower()
    main(category_arg)
