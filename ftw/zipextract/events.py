from ftw.zipextract.interfaces import IFile
from ftw.zipextract.interfaces import IZip
from Products.Five.utilities.marker import mark


def set_zip_on_creation(file, event):
    if IFile(file).is_zip():
        mark(file, IZip)
