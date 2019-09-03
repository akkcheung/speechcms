from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size

    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value

def validate_file_extension(value):

    import os
    ext = os.path.splitext(value.name)[1]

    valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg']
    if not ext in valid_extensions:
        raise ValidationError(u'File type not supported!')

    else:
        return value
