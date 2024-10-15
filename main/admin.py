from django.contrib import admin

# Register your models here.
from .models import Experiment, Sample,Sample_Metadata,Read_Pair, Titer

#admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(Sample_Metadata)
admin.site.register(Experiment)
admin.site.register(Read_Pair)
admin.site.register(Titer)