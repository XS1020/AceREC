import json
import os

from backend.settings import BASE_DIR

Mapping_Path = os.path.join(BASE_DIR, 'mapping.json')

Paper_Pdf_Mapping = {}
with open(Mapping_Path) as Fin:
	Paper_Pdf_Mapping = json.load(Fin)
	