import unittest
import json
import os

import dotrelay

with dotrelay.Radio(__file__) as rad:  # 📻
    ROOT_PATH = rad.resolved_path
    import cattlelyst as C

FIXTURES_PATH = os.path.join(ROOT_PATH, "tests/fixtures")


class TestEverything(unittest.TestCase):
    def test_base(self):
        """apply revgen algorithm to end state and compare results to expected prev states"""

        with open(os.path.join(FIXTURES_PATH, "tiles.json")) as fp:
            tiles = json.load(fp)

        with open(os.path.join(FIXTURES_PATH, "end_state.json")) as fp:
            end_state = json.load(fp)

        with open(
            os.path.join(FIXTURES_PATH, "expected_prev_states_by_uuid.json")
        ) as fp:
            expected_prev_state_by_uuid = json.load(fp)

        prev_state_by_uuid = C.dont_have_a_cow.generate_past_world_state_by_uuid(
            end_state, tiles
        )

        self.assertEqual(prev_state_by_uuid, expected_prev_state_by_uuid)


unittest.main()
