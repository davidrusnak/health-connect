import asyncio
import base64
import json
from typing import Dict, List
from fhirpy import AsyncFHIRClient


async def main():
    # Create an instance
    client = AsyncFHIRClient(
        'http://localhost:32783/fhir/r4',
    )

    await get_patients(client)

    #########################

    """
    test = await client.resources('MedicationRequest') \
    .include('MedicationDispense', 'prescription') \
    .include('MedicationRequest', 'performer', iterate=True) \
    .fetch_raw()

    print(json.dumps(list(test)[0], indent=4))
    """

    #########################

    to_get_list = ['Observation', 'Condition', 'Procedure', 'ServiceRequest', 'Encounter', 'DiagnosticReport', "Practitioner"]
    resource_dict = await get_patient_data(client, '36', to_get_list)
    # print key and the lenght of the inner list
    for key, value in resource_dict.items():
        print(f"{key}: {len(value)}")

    #########################

    # await send_service_request(client)

    #########################

    # await get_practitioners(client)
    """"
    to_get_list_practitioner = ['Patient', 'Condition', 'Procedure', 'ServiceRequest', 'Encounter', 'DiagnosticReport']
    resource_dict_practitioner = await get_practitioner_data(client, '1258', to_get_list_practitioner)
    # print key and the lenght of the inner list
    for key, value in resource_dict_practitioner.items():
        print(f"{key}: {len(value)}")
    """


async def get_patients(client: AsyncFHIRClient):
    resources = client.resources('Patient')
    patients = await resources.fetch_all()

    for patient in patients:
        # Convert the patient resource to a dictionary
        patient_dict = (await patient.to_resource())
        print(patient_dict)

        #print(json.dumps(patient_dict, indent=4))

async def send_service_request(client: AsyncFHIRClient):
    # Step 1: Search for the Patient resource with ID 36
    patient = await client.resources('Patient').search(_id='36').first()
    print(patient)

    if not patient:
        raise ValueError("Patient with ID 36 not found.")

    # Step 2: Read the image file and encode it in Base64
    with open('coffee.png', 'rb') as image_file:
        photo_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Step 3: Create the DocumentReference resource for the photo
    """
    photo_document = client.resource(
        resource_type='DocumentReference',
        status='current',
        type={
            'coding': [{
                'system': 'http://loinc.org',
                'code': '55114-3',  # Code for "Image Document"
                'display': 'Image Document'
            }]
        },
        subject={
            'reference': f'Patient/{patient["id"]}'
        },
        content=[{
            'attachment': {
                'contentType': 'image/png',  # Update MIME type for a PNG file
                'data': photo_data  # Base64-encoded photo data
            }
        }]
    )

    """
    photo_document = client.resource(
        resource_type= "DocumentReference",
        status= "final",
        type= {
            "coding": [
            {
                "system": "http://loinc.org",
                "code": "11488-4",
                "display": "Consultation Note"
            }
            ],
            "text": "Consultation Note"
        },
        subject= {
            "reference": "Patient/eXbMln3hu0PfFrpv2HgVHyg3"    
        },
        content= [
            {
            "attachment": {
                "contentType": "text/plain",
                "data": "SGVyZSBpcyBzb21lIE5vdGUgVGV4dCBpbiBoZXJlLCBlbmNvZGVkIHRvIGJhc2U2NCBmb3JtYXQuLi4="
            }
            }
        ],
        context= {
            "encounter": [{
            "reference": "Encounter/e0EueTd5RhhXyykueyj0Axg3"
            }]
        }
    )

    # Attempt to save the DocumentReference
    try:
        await photo_document.save()
        print("DocumentReference created with ID:", photo_document["id"])
    except Exception as e:
        print("Failed to create DocumentReference:", e)
        return  # Exit if saving DocumentReference fails

    # Step 4: Create the ServiceRequest resource
    service_request = client.resource(
        resource_type='ServiceRequest',
        status='active',
        intent='order',
        code={
            'coding': [{
                'system': 'http://snomed.info/sct',
                'code': '171055003',  # Code for "Diagnostic imaging request"
                'display': 'Diagnostic imaging request'
            }]
        },
        subject={
            'reference': f'Patient/{patient["id"]}'
        },
        supportingInfo=[{
            'reference': f'DocumentReference/{photo_document["id"]}'
        }]
    )

    # Attempt to save the ServiceRequest
    await service_request.save()
    print("ServiceRequest created with ID:", service_request["id"])

async def fetch_resources(client: AsyncFHIRClient, patient, resource_type: str):
    """Fetch all resources of a specified type for the given patient."""
    return await client.resources(resource_type).search(subject=patient).fetch_all()

async def print_get_resources_patient(resource_name: str, resources: List):
    """Print resources in JSON format."""
    print(f"{resource_name}:")
    resource_list = [await resource.to_resource() for resource in resources]
    for resource in resource_list:
        if (resource_name != 'XXXXX'):
            print(resource)
            print(json.dumps(resource, indent=4))

    return resource_list

async def get_patient_data(client: AsyncFHIRClient, patient_id: str, resource_types: List[str]):
    """Main function to retrieve and print patient data for given resource types."""
    # Fetch patient
    patient = await client.resources('Patient').get(patient_id)

    # Fetch and print resources based on provided types
    resource_dict = {}
    for resource_type in resource_types:
        resources = await fetch_resources(client, patient, resource_type)
        resource_dict[resource_type] = await print_get_resources_patient(resource_type, resources)

    return resource_dict

async def get_practitioners(client: AsyncFHIRClient):
    practitioner = await client.resources('Practitioner').get('1258')
    print(practitioner)

    print(json.dumps(await practitioner.to_resource(), indent=4))


##############

async def fetch_resources_for_practitioner(client: AsyncFHIRClient, practitioner, resource_type: str):
    """Fetch all resources of a specified type for the given practitioner."""
    return await client.resources(resource_type).search(subject=practitioner).fetch_all()

async def print_get_resources_practitioner(resource_name: str, resources: List):
    """Print resources in JSON format."""
    print(f"{resource_name}:")
    resource_list = [await resource.to_resource() for resource in resources]
    for resource in resource_list:
        if resource_name == 'XXXXX':
            print(resource)
            print(json.dumps(resource, indent=4))
    return resource_list

async def get_practitioner_data(client: AsyncFHIRClient, practitioner_id: str, resource_types: List[str]) -> Dict[str, List[Dict]]:
    """Main function to retrieve and print practitioner data for given resource types."""
    # Fetch practitioner
    practitioner = await client.resources('Practitioner').get(practitioner_id)

    # Fetch and print resources based on provided types
    resource_dict = {}
    for resource_type in resource_types:
        resources = await fetch_resources_for_practitioner(client, practitioner, resource_type)
        resource_dict[resource_type] = await print_get_resources_practitioner(resource_type, resources)

    return resource_dict

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())