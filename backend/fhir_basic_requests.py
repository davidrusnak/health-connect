import asyncio
import base64
import json
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

    await get_thingies(client)

    #########################

    # await send_service_request(client)

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

async def get_thingies(client: AsyncFHIRClient):
    patient_id = '36'  # Replace with the actual patient ID you want to query

    # get patient
    patient = await client.resources('Patient').get(patient_id)
    #print(patient)

    observations = await client.resources('Observation').search(subject=patient).fetch_all()
    #print(observations)

    # Fetch all observations for the specified patient
    # observations = await (await client.resources('Observation').search(subject=patient_id)).fetch_all()
    

    # Fetch all conditions for the specified patient
    conditions = await client.resources('Condition').search(subject=patient).fetch_all()

    # Fetch all procedures for the specified patient
    procedures = await client.resources('Procedure').search(subject=patient).fetch_all()

    service_requests = await client.resources('ServiceRequest').search(subject=patient).fetch_all()

    diagnostic_requests = await client.resources('DiagnosticReport').search(subject=patient).fetch_all()
    print("DiagnosticReports:")
    for diagnostic_report in diagnostic_requests:
        print(diagnostic_report)
        print(json.dumps(await diagnostic_report.to_resource(), indent=4))

    print("ServiceRequests:")
    for service_request in service_requests:
        print(service_request)
        print(json.dumps(await service_request.to_resource(), indent=4))

    # Print all observations
    print("Observations:")
    for obs in observations:
        break
        print(obs)
        #print(json.dumps(await obs.to_resource(), indent=4))

    # Print all conditions
    print("\nConditions:")
    for condition in conditions:
        break
        print(condition)
        #print(json.dumps(await condition.to_resource(), indent=4))

    # Print all procedures
    print("\nProcedures:")
    for procedure in procedures:
        break
        print(procedure)
        #print(json.dumps(await procedure.to_resource(), indent=4))

    # Search for all ServiceRequests for the specified patient
    service_requests = await client.resources('ServiceRequest').search(subject=f'Patient/{patient_id}').fetch()

    # Print details of each ServiceRequest
    for sr in service_requests:
        print(f"ServiceRequest ID: {sr.id}")
        print(f"Status: {sr['status']}")
        print(f"Intent: {sr['intent']}")
        print(f"Code: {sr['code']['coding'][0]['display'] if sr['code'] and sr['code']['coding'] else 'N/A'}")
        print(f"Supporting Info: {sr.get('supportingInfo', [])}")
        print("-" * 40)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())