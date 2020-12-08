import json
import pkg_resources


__all__ = ["QE_TAGS"]


tags_file = pkg_resources.resource_filename(
    "dftinputgen.qe.settings", "tags_and_groups.json"
)
with open(tags_file, "r") as fr:
    QE_TAGS = json.load(fr)
