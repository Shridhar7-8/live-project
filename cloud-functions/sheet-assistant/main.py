# import gspread
# from google.oauth2.service_account import Credentials
# import os

# def get_customer_data(customer_id: str, sheet_name: str = 'Synthetic_Bank_Customer_Records_new') -> dict:
#     """
#     Retrieves customer data from Google Sheets using Account ID.
    
#     Args:
#         customer_id (str): The customer's account ID to search
#         sheet_name (str): Name of the Google Sheet
    
#     Returns:
#         dict: Customer data or error message
#     """
#     print(f"\n[TOOL] Called get_customer_data with ID: {customer_id}, Sheet: {sheet_name}")
#     service_account_file = '/home/itel/Downloads/audio-gemini/server/config/service_account.json'
    
#     # Check if service account file exists
#     if not os.path.exists(service_account_file):
#         print(f"[TOOL_ERROR] Service account file '{service_account_file}' not found.")
#         return {"error": f"Configuration error: Service account file '{service_account_file}' not found."}
        
#     try:
#         # Updated scope for modern Google Sheets API
#         scope = [
#             'https://www.googleapis.com/auth/spreadsheets',
#             'https://www.googleapis.com/auth/drive'
#         ]

#         # Authenticate
#         creds = Credentials.from_service_account_file(
#             service_account_file, 
#             scopes=scope
#         )
#         client = gspread.authorize(creds)

#         # Access sheet
#         print(f"[TOOL] Accessing Google Sheet: {sheet_name}")
#         sheet = client.open(sheet_name).sheet1
        
#         # More efficient search using gspread's find method
#         try:
#             print(f"[TOOL] Searching for customer ID: {customer_id} in column 1")
#             cell = sheet.find(str(customer_id), in_column=1)  # Assuming Account Id is in Column 1
#             print(f"[TOOL] Found customer ID at row: {cell.row}")
#             record_values = sheet.row_values(cell.row)
            
#             # Map to your column headers (assuming headers are in row 1)
#             headers = sheet.row_values(1)
#             record_dict = dict(zip(headers, record_values))
           
#             return record_dict
            
#         except gspread.exceptions.CellNotFound:
#             print(f"[TOOL_ERROR] Account ID {customer_id} not found in sheet.")
#             return {"error": "Account ID not found"}
#         except gspread.exceptions.APIError as api_e:
#             print(f"[TOOL_ERROR] Google Sheets API error during find/read: {api_e}")
#             return {"error": f"Google Sheets API error: {str(api_e)}"}

#     except gspread.exceptions.SpreadsheetNotFound:
#         print(f"[TOOL_ERROR] Spreadsheet '{sheet_name}' not found or permission denied.")
#         return {"error": f"Spreadsheet '{sheet_name}' not found or permission denied."}
#     except Exception as e:
#         print(f"[TOOL_ERROR] Unexpected error in get_customer_data: {e}")
#         return {"error": f"Service error: {str(e)}"}


# if __name__ == "__main__":
#     test_account_id = "999999006"
#     result = get_customer_data(test_account_id)
#     print("Test Oautput for Account ID", test_account_id)
#     print(result)



# main.py
import os
from google.auth import default
from googleapiclient.discovery import build
from flask import Request, jsonify

def get_customer_data(request: Request):
    """
    HTTP Cloud Function to retrieve a row from a Google Sheet matching customer_id.
    Expects query parameters:
      - customer_id: the account ID to search for (required)
    Returns:
      JSON object of the row data (with keys from header row), or error info.
    """
    # Hardcoded spreadsheet configuration
    SPREADSHEET_ID = "1pdRzL87kMaGBQQbZJv4h4GB8QIXLEP0o81yQ164GHdM"
    SHEET_NAME = "Synthetic_Bank_Customer_Records.csv"
    
    # 1. Parse parameters
    customer_id = request.args.get("customer_id")

    if not customer_id:
        return jsonify({"error": "Missing 'customer_id' parameter"}), 400

    # 2. Acquire ADC credentials with appropriate scopes
    try:
        credentials, project = default(scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    except Exception as e:
        return jsonify({"error": f"Failed to acquire credentials: {e}"}), 500

    # 3. Build Sheets API client
    try:
        sheets_service = build('sheets', 'v4', credentials=credentials)
    except Exception as e:
        return jsonify({"error": f"Failed to build Sheets service: {e}"}), 500

    # 4. Read header row (row 1) to get column names
    header_range = f"{SHEET_NAME}!1:1"
    try:
        header_resp = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=header_range
        ).execute()
        headers = header_resp.get("values", [[]])
        if not headers or not headers[0]:
            return jsonify({"error": f"No header row found in sheet '{SHEET_NAME}'"}), 500
        headers = headers[0]  # list of column names
    except Exception as e:
        return jsonify({"error": f"Error reading header row: {e}"}), 500

    # 5. Read the ID column (assumed column A). We skip header, so start from row 2.
    id_column_range = f"{SHEET_NAME}!A2:A"
    try:
        id_resp = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=id_column_range
        ).execute()
        id_values = id_resp.get("values", [])  # list of [cell_value] for each row
    except Exception as e:
        return jsonify({"error": f"Error reading ID column: {e}"}), 500

    # 6. Search for the requested customer_id in the ID column
    found_row_index = None
    target = str(customer_id)
    for idx, row in enumerate(id_values):
        if not row:
            continue
        if str(row[0]) == target:
            found_row_index = idx + 2  # actual sheet row number (since idx=0 => row 2)
            break

    if found_row_index is None:
        return jsonify({"error": f"Account ID '{customer_id}' not found"}), 404

    # 7. Read the entire row at found_row_index
    row_range = f"{SHEET_NAME}!{found_row_index}:{found_row_index}"
    try:
        row_resp = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=row_range
        ).execute()
        row_values = row_resp.get("values", [[]])
        if not row_values or not row_values[0]:
            return jsonify({"error": f"No data found in row {found_row_index}"}), 500
        row_values = row_values[0]  # list of cell values in that row
    except Exception as e:
        return jsonify({"error": f"Error reading row {found_row_index}: {e}"}), 500

    # 8. Map headers to row values
    record = {}
    for col_index, header in enumerate(headers):
        record[header] = row_values[col_index] if col_index < len(row_values) else ""

    return jsonify(record)
