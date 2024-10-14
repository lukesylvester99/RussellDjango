from django.shortcuts import render
from ninja import NinjaAPI, Schema
from main.models import Sample, Read_Pair, Sample_Metadata, Titer

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
    

class TiterSchema(Schema):
    sample_id: str
    sequencing_run: str
    wri_mean_depth: int
    dmel_mean_depth: int
    wri_titer: int
    total_reads: int
    mapped_reads: int
    duplicate_reads: int
    wmel_mean_depth: int
    wwil_mean_depth: int
    wmel_titer: int
    wwil_titer: int
    dsim_mean_depth: int

@api.post("/receive-titer/")
def receive_paths(request, payload: TiterSchema):
    try:
        # Extract values from the payload
        sample_id = payload.sample_id
        sequencing_run = payload.sequencing_run
        wri_mean_depth = payload.wri_mean_depth
        dmel_mean_depth = payload.dmel_mean_depth
        wri_titer = payload.wri_titer
        total_reads = payload.total_reads
        mapped_reads = payload.mapped_reads
        duplicate_reads = payload.duplicate_reads
        wmel_mean_depth = payload.wmel_mean_depth
        wwil_mean_depth = payload.wwil_mean_depth
        wmel_titer = payload.wmel_titer
        wwil_titer = payload.wwil_titer
        dsim_mean_depth = payload.dsim_mean_depth

        sample = Sample.objects.get(sample_id=sample_id)
        titer, created = Titer.objects.update_or_create(
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
        return {"success": True, "message": "Titers received and saved!"}
    
    except Sample.DoesNotExist:
        return {"success": False, "message": "Sample ID not found!"}
    