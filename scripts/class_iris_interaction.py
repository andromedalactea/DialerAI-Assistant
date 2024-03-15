# Import standard libraries
import os

# Import third-party libraries
import requests
from dotenv import load_dotenv

# Charge the environment variables
load_dotenv()


class IrisCRM:
    """
    Class to interact with the Iris CRM API.

    Attributes:
        url (str): The base URL for the API.
        X_API_KEY (str): The API key required for authentication.
    """
    def __init__(self):
        self.url = "https://aventus.iriscrm.com/api/v1/leads"
        self.X_API_KEY = os.getenv('X_API_KEY_IRIS_CRM')

    def get_leads_list_by_category(self, id_category, id_status):
        """
        Makes a GET request to the specified URL to fetch leads data by category.

        Uses a set of predefined headers including the User-Agent and X-API-KEY,
        required by the API. The category filtering should be implemented according
        to the API documentation, which might involve adjusting the URL or parameters.

        Returns:
            list: The lead ID for each lead in the response.
        """
        url = "https://aventus.iriscrm.com/api/v1/leads?"
        headers = {
            "User-Agent": "Vapi",
            "X-API-KEY": self.X_API_KEY,
            "accept": "application/json",
        }

        params = {
            "status": id_status,
            "category": id_category,
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            ids = [dic['id'] for dic in data.get('data', []) if 'id' in dic]
            return ids
        else:
            print(f"Error fetching data: {response.status_code}")
            return []

    def get_info_by_lead(self, lead_id, skip_empty_set=1):
        """
        Fetches detailed information for a specific lead by its ID.

        Args:
            lead_id (int): The unique identifier for the lead.
            skip_empty_set (int, optional): Indicates whether to skip empty sets in the response.
                Use 1 to skip, 0 to include. Defaults to 0.

        Returns:
            dict: The detailed information of the lead if the request is successful, otherwise an error message.
        """
        url = f"{self.url}/{lead_id}"
        headers = {
            "X-API-KEY": self.X_API_KEY,
            "accept": "application/json",
        }
        params = {
            "skip_empty_set": skip_empty_set
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Extract phones of the structure of response by the id of the fields
        desired_ids = {7027, 7009, 11108, 7010}  # 7027: Contact Phone, 7009: Mobile, 11108: Work, 7010: Other

        # General Information
        name_company = data['general']['name']

        # List to store the extracted dictionaries
        extracted_info_per_number = []

        # Iterate through each item in 'details' and then in 'fields'
        for item in data['details']:
            for field in item['fields']:
                if field['id'] in desired_ids:
                    extracted_info_per_number.append(field)

        phones_non_empty = ["+1" + d['value'].replace("-", "") for d in extracted_info_per_number if d['value'] != ""]

        complete_info = {
            "id_lead": lead_id,
            "name_company": name_company,
            "phones": phones_non_empty
        }

        return complete_info

    def extract_info_for_a_list_of_leads(self, list_lead_id, skip_empty_set=1):
        """
        Fetches detailed information for a specific lead by its ID.

        Args:
            lead_id (int): The unique identifier for the lead.
            skip_empty_set (int, optional): Indicates whether to skip empty sets in the response.
                Use 1 to skip, 0 to include. Defaults to 0.

        Returns:
            dict: The detailed information of the lead if the request is successful, otherwise an error message.
        """
        info_extracted = []
        for lead_id in list_lead_id:
            info_extracted.append(self.get_info_by_lead(lead_id, skip_empty_set))

        return info_extracted

    def create_note_for_lead(self, lead_id, number, date, ended_reason, transcript, summary):
        """
        Creates a note for a lead in the system.

        Parameters:
        lead_id (int): The ID of the lead.
        number (str): The called number.
        date (str): The date of the call.
        ended_reason (str): The reason the call ended.
        transcript (str): The transcript of the call.
        summary (str): A summary of the call.

        Returns:
        response (requests.Response): The response object from the API requests.
        """
        url = f"{self.url}/{lead_id}/notes"
        headers = {
            "X-API-KEY": self.X_API_KEY,
            "accept": "application/json",
        }

        note = f"""
        Called_number: {number}
        Date: {date}
        Ended_reason: {ended_reason}
        Transcript: {transcript}\n
        Summary: {summary}
        """

        payload = {
            "tab": 2,
            "note": note,
            "sticky": "No"
        }

        response = requests.post(url, headers=headers, json=payload)

        return response


# Example usage
if __name__ == "__main__":
    id_category = "17"   # id for "Qualifying"
    id_status = "331"    # id for "Time Filler"
    # Initialize the class
    iris = IrisCRM()
    leads = iris.get_leads_list_by_category(id_category, id_status)

    # Extract info for each lead
    info_leads = iris.extract_info_for_a_list_of_leads(leads, skip_empty_set=1)
    print(info_leads)
