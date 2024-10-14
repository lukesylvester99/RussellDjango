from django.shortcuts import render
from ninja import NinjaAPI, Schema
from main.models import Sample, Read_Pair

api = NinjaAPI()

class PathSchema(Schema):
    sample_id: str
    read1_path: str
    read2_path: str

@api.post("/receive-paths/")
def receive_paths(request, payload: PathSchema):
    try:
        # Extract values from the payload
        sample_id = payload.sample_id
        read1_path = payload.read1_path
        read2_path = payload.read2_path

        sample = Sample.objects.get(sample_id=sample_id)
        read_pair, created = Read_Pair.objects.update_or_create(
            sample_id=sample,
            defaults={'read1_path': read1_path, 'read2_path': read2_path}
        )
        return {"success": True, "message": "Paths received and saved!"}
    
    except Sample.DoesNotExist:
        return {"success": False, "message": "Sample ID not found!"}

