import os
import glob
import json
import pkg_resources


__all__ = ["QE_PRESETS"]


presets_jsons = glob.glob(
    pkg_resources.resource_filename(
        "dftinpgen.qe.settings.calculation_presets", "*.json"
    )
)


QE_PRESETS = {}
for presets_json in presets_jsons:
    presets_name = os.path.splitext(os.path.basename(presets_json))[0]
    with open(presets_json, "r") as fr:
        QE_PRESETS[presets_name] = json.load(fr)
