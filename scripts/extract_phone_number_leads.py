import requests
import os

def get_Phones_by_lead_info(list_lead_id, skip_empty_set=1):
    """
    Fetches detailed information for a specific lead by its ID.

    Args:
        lead_id (int): The unique identifier for the lead.
        skip_empty_set (int, optional): Indicates whether to skip empty sets in the response.
            Use 1 to skip, 0 to include. Defaults to 0.

    Returns:
        dict: The detailed information of the lead if the request is successful, otherwise an error message.
    """
    url = f"https://aventus.iriscrm.com/api/v1/leads/{lead_id}"
    headers = {
        "X-API-KEY": os.getenv('X_API_KEY_IRIS_CRM'),
        "accept": "application/json",
    }
    params = {
        "skip_empty_set": skip_empty_set
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Para extraer el valor de 'name' de 'status':
    status_name = data['general']['status']['name']
    print("Status Name:", status_name)

    # Para extraer el valor de 'Contact Phone' de 'fields':
    # Primero, accedemos a la lista de 'details', luego a la primera entrada ('fields'), y iteramos hasta encontrar el campo deseado.
    contact_phone = None
    for field in data['details'][0]['fields']:  # Asumiendo que el campo está en el primer elemento de 'details'
        if field['field'] == 'Contact Phone':
            contact_phone = field['value']
            break

    Bussines_phone = None
    for field in data['details'][0]['fields']:  # Asumiendo que el campo está en el primer elemento de 'details'
        if field['field'] == 'Business Phone':
            Bussines_phone = field['value']
            break        
    print("Bussines Phone:", Bussines_phone)
    print("Contact Phone:", contact_phone)
    if response.status_code == 200:
        return  None  # Returns the detailed lead information
    else:
        return {"error": f"Failed to fetch lead info, status code: {response.status_code}"}

# Example usage
lead_id = 194  # Replace 12345 with the actual lead ID you want to fetch
detailed_info = get_detailed_lead_info(lead_id, skip_empty_set=1)  # Example with skipping empty sets
print(detailed_info)
