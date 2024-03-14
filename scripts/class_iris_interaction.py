import os

import requests

class iris_crm:
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
            list id: The lead ID for each lead in the response.
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
        # print(response.json())
        if response.status_code == 200:
            data = response.json()
            print(data)
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
        # print(data)

        # Extract phones of the structure of response by the id of the fields
        ids_deseados = {7027, 7009, 11108, 7010} 

        # Lista para guardar los diccionarios extraídos
        extract_info_per_number = []

        # Iterar a través de cada elemento en 'details' y luego en 'fields'
        for item in data['details']:
            for field in item['fields']:
                if field['id'] in ids_deseados:
                    extract_info_per_number.append(field)
        
        Phones_no_empty = [d['value'] for d in extract_info_per_number if d['value'] != ""]

        print(Phones_no_empty)

    def extract_info_for_a_list_of_leads(self, list_lead_id, status_name_required, skip_empty_set=1):
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
    
# Example usage
if __name__ == "__main__":
    id_category = "17"   # id for "Qualifying"
    id_status = "331"    # id for "Time Filler"
    # Initialize the class
    iris = iris_crm()
    leads = iris.get_leads_list_by_category(id_category, id_status)
    
    # Extract info for each lead
    info_leads = iris.extract_info_for_a_list_of_leads(leads, "Time Filler Leads", skip_empty_set=1)
    print(info_leads)
