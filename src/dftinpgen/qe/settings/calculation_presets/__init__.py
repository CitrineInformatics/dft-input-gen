import os
import glob
import json


__all__ = ["QE_PRESETS"]


presets_jsons = glob.glob(os.path.join(os.path.dirname(__file__), "*.json"))

QE_PRESETS = {}
for presets_json in presets_jsons:
    presets_name = os.path.splitext(os.path.basename(presets_json))[0]
    with open(presets_json, "r") as fr:
        QE_PRESETS[presets_name] = json.load(fr)
