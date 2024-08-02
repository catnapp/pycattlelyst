import json
import os

import dotrelay

with dotrelay.Radio(__file__) as rad:  # 📻
    ROOT_PATH = rad.resolved_path
    import cattlelyst as C

SCRIPTS_PATH = os.path.join(ROOT_PATH, "scripts")

# process raw world states

with open(os.path.join(SCRIPTS_PATH, "world_states", "raw.json")) as fp:
    STATES = json.load(fp)

world_state_by_uuid = {C.helpers.hash_world_state(state): state for state in STATES}

with open(os.path.join(SCRIPTS_PATH, "world_states", "by_uuid.json"), "w") as fp:
    json.dump(world_state_by_uuid, fp, indent=4)


# process raw cows

with open(os.path.join(SCRIPTS_PATH, "cows", "raw.json")) as fp:
    COWS = json.load(fp)

cow_by_uuid = {C.helpers.hash_uuidable(cow): cow for cow in COWS}

with open(os.path.join(SCRIPTS_PATH, "cows", "by_uuid.json"), "w") as fp:
    json.dump(cow_by_uuid, fp, indent=4)
