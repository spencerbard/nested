""" Test nested """
import json
from pkg import get_map, nflatten_map, nmerge_concat, get_groups

TEST_ITEMS = [
    {"id": 1, "team_id": 1, "is_pitcher": 0, "name": "Test Person 1"},
    {"id": 2, "team_id": 1, "is_pitcher": 1, "name": "Test Person 2"},
    {"id": 3, "team_id": 1, "is_pitcher": 1, "name": "Test Person 3"},
    {"id": 4, "team_id": 2, "is_pitcher": 1, "name": "Test Person 4"},
    {"id": 5, "team_id": 3, "is_pitcher": 1, "name": "Test Person 5"},
]


def test_nmerge_concat():
    _dict = {
        "somethingelse": {"batter": [10, 9, 8]},
        "xwoba": {"batter": [1000, 1001, 1002]},
    }
    nmerge_concat(_dict, {"xwoba": {"batter": [1, 2, 3], "pitcher": [4, 5, 6]}})
    nmerge_concat(_dict, {"xwoba": {"batter": [7, 8, 9], "pitcher": [10, 11, 12]}})
    assert json.dumps(_dict) == json.dumps(
        {
            "somethingelse": {"batter": [10, 9, 8]},
            "xwoba": {
                "batter": [1000, 1001, 1002, 1, 2, 3, 7, 8, 9],
                "pitcher": [4, 5, 6, 10, 11, 12],
            },
        }
    )


def test_get_map():
    team_map = get_map(TEST_ITEMS, ["team_id"])
    print(json.dumps(team_map))
    assert json.dumps(team_map) == json.dumps(
        {
            1: [
                {"id": 1, "team_id": 1, "is_pitcher": 0, "name": "Test Person 1"},
                {"id": 2, "team_id": 1, "is_pitcher": 1, "name": "Test Person 2"},
                {"id": 3, "team_id": 1, "is_pitcher": 1, "name": "Test Person 3"},
            ],
            2: [{"id": 4, "team_id": 2, "is_pitcher": 1, "name": "Test Person 4"}],
            3: [{"id": 5, "team_id": 3, "is_pitcher": 1, "name": "Test Person 5"}],
        }
    )
    team_pitcher_map = get_map(TEST_ITEMS, ["team_id", "is_pitcher"])
    assert json.dumps(team_pitcher_map) == json.dumps(
        {
            1: {
                0: [{"id": 1, "team_id": 1, "is_pitcher": 0, "name": "Test Person 1"}],
                1: [
                    {"id": 2, "team_id": 1, "is_pitcher": 1, "name": "Test Person 2"},
                    {"id": 3, "team_id": 1, "is_pitcher": 1, "name": "Test Person 3"},
                ],
            },
            2: {1: [{"id": 4, "team_id": 2, "is_pitcher": 1, "name": "Test Person 4"}]},
            3: {1: [{"id": 5, "team_id": 3, "is_pitcher": 1, "name": "Test Person 5"}]},
        }
    )


def test_nflatten_map():
    team_map = get_map(TEST_ITEMS, ["team_id"])
    team_groups = nflatten_map(team_map)
    assert json.dumps(team_groups) == json.dumps(
        [
            [
                {"id": 1, "team_id": 1, "is_pitcher": 0, "name": "Test Person 1"},
                {"id": 2, "team_id": 1, "is_pitcher": 1, "name": "Test Person 2"},
                {"id": 3, "team_id": 1, "is_pitcher": 1, "name": "Test Person 3"},
            ],
            [{"id": 4, "team_id": 2, "is_pitcher": 1, "name": "Test Person 4"}],
            [{"id": 5, "team_id": 3, "is_pitcher": 1, "name": "Test Person 5"}],
        ]
    )


def test_get_groups():
    groups_no_keys_1 = get_groups(TEST_ITEMS, ["team_id"])
    assert json.dumps(groups_no_keys_1) == json.dumps(
        [
            [
                {"id": 1, "team_id": 1, "is_pitcher": 0, "name": "Test Person 1"},
                {"id": 2, "team_id": 1, "is_pitcher": 1, "name": "Test Person 2"},
                {"id": 3, "team_id": 1, "is_pitcher": 1, "name": "Test Person 3"},
            ],
            [{"id": 4, "team_id": 2, "is_pitcher": 1, "name": "Test Person 4"}],
            [{"id": 5, "team_id": 3, "is_pitcher": 1, "name": "Test Person 5"}],
        ]
    )
    groups_no_keys_2 = get_groups(TEST_ITEMS, ["team_id", "is_pitcher"])
    assert json.dumps(groups_no_keys_2) == json.dumps(
        [
            [{"id": 1, "team_id": 1, "is_pitcher": 0, "name": "Test Person 1"}],
            [
                {"id": 2, "team_id": 1, "is_pitcher": 1, "name": "Test Person 2"},
                {"id": 3, "team_id": 1, "is_pitcher": 1, "name": "Test Person 3"},
            ],
            [{"id": 4, "team_id": 2, "is_pitcher": 1, "name": "Test Person 4"}],
            [{"id": 5, "team_id": 3, "is_pitcher": 1, "name": "Test Person 5"}],
        ]
    )
    groups_w_keys_2 = get_groups(
        TEST_ITEMS, ["team_id", "is_pitcher"], include_keys=True
    )
    assert json.dumps(groups_w_keys_2) == json.dumps(
        [
            (
                (1, 0),
                [{"id": 1, "team_id": 1, "is_pitcher": 0, "name": "Test Person 1"}],
            ),
            (
                (1, 1),
                [
                    {"id": 2, "team_id": 1, "is_pitcher": 1, "name": "Test Person 2"},
                    {"id": 3, "team_id": 1, "is_pitcher": 1, "name": "Test Person 3"},
                ],
            ),
            (
                (2, 1),
                [{"id": 4, "team_id": 2, "is_pitcher": 1, "name": "Test Person 4"}],
            ),
            (
                (3, 1),
                [{"id": 5, "team_id": 3, "is_pitcher": 1, "name": "Test Person 5"}],
            ),
        ]
    )


if __name__ == "__main__":
    test_get_groups()
