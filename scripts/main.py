# This is the main script that will be called by the cron job

# Import standard libraries
import time

# Local libraries
from class_iris_interaction import IrisCRM
from call_ai import call_ai

# Main flux dialer
def main_flux_dialer(id_category, id_status):
    """
    This function is the main script that will be called by the cron job.
    It gets the leads from the CRM and calls the AI assistant for each lead.

    Args:
        id_category (str): The ID of the category to filter the leads.
        id_status (str): The ID of the status to filter the leads.
    
    Returns:
        str: A message indicating that the process has finished.
    """
    # Initialize the class
    iris = IrisCRM()  # This is the class that interacts with the CRM
    leads = iris.get_leads_list_by_category(id_category, id_status)

    # Calling info for each lead
    for lead_id in leads:
        lead = iris.get_info_by_lead(lead_id, skip_empty_set=1)

        # Extract general information
        customer_id = lead["id_lead"]
        name = lead["name_company"]
        # Extract the first phone number
        phone_number = lead["phones"][0] if lead["phones"] else None

        if phone_number is not None:
            # call = call_ai(customer_id, phone_number)
            call = "Call made"
            if call == "Call made":
                print(f"Called {phone_number} for customer {name}")
                time.sleep(5) # To don't exceed the API rate limit
        else:
            print(f"No phone number for customer {name}")
            continue
    return "Process finished."

# Example usage
if __name__ == "__main__":
    id_category = "17"   # id for "Qualifying"
    id_status = "331"    # id for "Time Filler"
    main_flux_dialer(id_category, id_status)
