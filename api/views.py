from django.shortcuts import render
from ninja import NinjaAPI, Schema
from main.models import Sample, Read_Pair, Sample_Metadata

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
    

@api.get("/get-cell-type/")
def get_cell_type(request, sample_id: str):
    try:
        metadata_obj = Sample_Metadata.objects.get(sample_id__sample_id=sample_id)
        metadata_dict = metadata_obj.metadata

        # Extract the cell type from the metadata
        cell_type = metadata_dict.get("Cell_Line", "Unknown") 

        return {"success": True, "sample_id": sample_id, "cell_type": cell_type}
    
    except Sample_Metadata.DoesNotExist:
        return {"success": False, "message": "Sample ID not found"}
    

