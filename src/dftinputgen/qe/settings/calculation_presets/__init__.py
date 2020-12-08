import os
import json
import pkg_resources


__all__ = ["QE_PRESETS"]


QE_PRESETS = {}


preset_listdir = pkg_resources.resource_listdir(
    "dftinputgen.qe.settings", "calculation_presets"
)
for filename in preset_listdir:
    root, ext = os.path.splitext(filename)
    if not ext == ".json":
        continue
    resource = pkg_resources.resource_filename(
        "dftinputgen.qe.settings.calculation_presets", filename
    )
    with open(resource, "r") as fr:
        QE_PRESETS[root] = json.load(fr)
