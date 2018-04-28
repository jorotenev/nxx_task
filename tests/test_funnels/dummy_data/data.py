import json
from tests.utils import get_directory_of_file

curr_dir = get_directory_of_file(__file__)

dummy_funnels = json.load(open("%s/funnels.json" % curr_dir))
dummy_funnels_enums = json.load(open("%s/funnels_enums.json" % curr_dir))
