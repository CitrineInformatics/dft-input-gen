import os
import json


__all__ = ['QE_TAGS']


tags_file = os.path.join(os.path.dirname(__file__), 'tags_and_groups.json')

with open(tags_file, 'r') as fr:
    QE_TAGS = json.load(fr)
