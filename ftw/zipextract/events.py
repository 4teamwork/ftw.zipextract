from interfaces import IFile
from interfaces import IZip
from Products.Five.utilities.marker import mark


def set_zip_on_creation(file, event):
    if IFile(file)._is_zip():
        mark(file, IZip)
