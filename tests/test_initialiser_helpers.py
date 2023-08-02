# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import pytest

from terminate_managers_init.find_no_engagement_managers import (
    extract_managers_with_no_persons_or_engagements,
)


@pytest.mark.parametrize(
    "test_data, expected_result",
    [
        (
            [
                {
                    "objects": [
                        {
                            "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                            "employee": [
                                {
                                    "engagements": [
                                        {"uuid": "ef9f76fd-1840-4d94-961a-1140c86efd00"}
                                    ]
                                }
                            ],
                            "validity": {
                                "from": "2020-07-18T00:00:00+02:00",
                                "to": None,
                            },
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "uuid": "3338a91f-5bc5-4a40-9675-cc65a74f3d30",
                            "employee": None,
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "uuid": "b7fab760-a679-49d0-8338-eff40f66c711",
                            "employee": [{"engagements": []}],
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "uuid": "2e9a7dff-4eed-4060-b746-cbf8e224bfb4",
                            "employee": [{"engagements": []}],
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "uuid": "e4c99547-4a5b-4423-a1dc-2fc5b3b68c35",
                            "employee": None,
                        }
                    ]
                },
            ],
            [
                "3338a91f-5bc5-4a40-9675-cc65a74f3d30",
                "b7fab760-a679-49d0-8338-eff40f66c711",
                "2e9a7dff-4eed-4060-b746-cbf8e224bfb4",
                "e4c99547-4a5b-4423-a1dc-2fc5b3b68c35",
            ],
        ),
        (
            [
                {
                    "objects": [
                        {
                            "uuid": "45fec51e-6bb9-475a-bdf7-ea16db20ebde",
                            "employee": [
                                {
                                    "engagements": [
                                        {"uuid": "589eb3a9-4ea4-43e7-aaaf-b3363a058c8b"}
                                    ]
                                }
                            ],
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "uuid": "4d28ab20-b4c1-4952-b3c2-b0661896dd2b",
                            "employee": [
                                {
                                    "engagements": [
                                        {"uuid": "638fdca9-7ed1-48f5-baad-b3d00f2ee765"}
                                    ]
                                }
                            ],
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "uuid": "556ea48a-a1cb-4200-957d-a9127858773e",
                            "employee": [
                                {
                                    "engagements": [
                                        {"uuid": "f4e531dc-7188-4813-9dfb-8a1397e374be"}
                                    ]
                                }
                            ],
                        }
                    ]
                },
            ],
            [],
        ),
    ],
)
def test_extract_managers_with_no_persons_or_engagements(test_data, expected_result):
    result = extract_managers_with_no_persons_or_engagements(test_data)
    assert result == expected_result
