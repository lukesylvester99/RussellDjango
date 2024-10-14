from django.db import models


class Experiment(models.Model):
    name = models.CharField(max_length=255)

class Sample(models.Model):
    sample_id = models.CharField(max_length=30)
    created_date = models.DateField()
    sample_label = models.CharField(max_length=150, default="")
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

class Sample_Metadata(models.Model):
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)
    metadata = models.JSONField()

class Read_Pair(models.Model):
    read1_path = models.CharField(max_length=255)
    read2_path = models.CharField(max_length=255)
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)
    plate_number = models.IntegerField()