from django.shortcuts import render
from ninja import NinjaAPI, Schema
from main.models import Sample, Read_Pair, Sample_Metadata, Titer
import pprint

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
    

@api.post("/receive-titer/")
def receive_titer(request, payload: list[dict]):
    pprint.pprint(payload)
    try:
        for row in payload:
            sample_id = row.get('SampleID')
            sequencing_run = row.get('sequencing_run')
            wri_mean_depth = float(row.get('wri_mean_depth') or 0.0)
            dmel_mean_depth = float(row.get('dmel_mean_depth') or 0.0)
            wri_titer = float(row.get('wri_titer') or 0.0)
            total_reads = int(row.get('total_reads') or 0)
            mapped_reads = int(row.get('mapped_reads') or 0)
            duplicate_reads = int(row.get('duplicate_reads') or 0)
            wmel_mean_depth = float(row.get('wmel_mean_depth') or 0.0)
            wwil_mean_depth = float(row.get('wwil_mean_depth') or 0.0)
            wmel_titer = float(row.get('wmel_titer') or 0.0)
            wwil_titer = float(row.get('wwil_titer') or 0.0)
            dsim_mean_depth = float(row.get('dsim_mean_depth') or 0.0)

            try:
                sample = Sample.objects.get(sample_id=sample_id)
                Titer.objects.update_or_create(
                    sample_id=sample,
                    defaults={
                        "sequencing_run": sequencing_run,
                        "wri_mean_depth": wri_mean_depth,
                        "dmel_mean_depth": dmel_mean_depth,
                        "wri_titer": wri_titer,
                        "total_reads": total_reads,
                        "mapped_reads": mapped_reads,
                        "duplicate_reads": duplicate_reads,
                        "wmel_mean_depth": wmel_mean_depth,
                        "wwil_mean_depth": wwil_mean_depth,
                        "wmel_titer": wmel_titer,
                        "wwil_titer": wwil_titer,
                        "dsim_mean_depth": dsim_mean_depth
                    }
                )
            except Sample.DoesNotExist:
                return {"success": False, "message": f"Sample ID {sample_id} not found!"}

        return {"success": True, "message": "Titer data received and saved!"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}
    