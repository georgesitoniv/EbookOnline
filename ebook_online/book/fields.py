from filer.fields.file import FilerFileField, AdminFileFormField

from filer_pdf import models

class FilerPDFField(FilerFileField):
    default_model_class = models.PDF