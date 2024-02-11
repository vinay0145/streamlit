# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re

import pytest
from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction


@pytest.mark.skip_browser("chromium")
def test_video_rendering(app: Page, assert_snapshot: ImageCompareFunction):
    """Test that `st.video` renders correctly via screenshots matching."""
    video_elements = app.get_by_test_id("stVideo")
    expect(video_elements).to_have_count(3)

    expect(video_elements.nth(0)).to_be_visible()
    expect(video_elements.nth(1)).to_be_visible()
    expect(video_elements.nth(2)).to_be_visible()

    assert_snapshot(video_elements.nth(0), name="video_element_first")
    assert_snapshot(video_elements.nth(1), name="video_element_second")
    assert_snapshot(video_elements.nth(2), name="video_element_third")


def test_displays_a_video_player(app: Page):
    video_element = app.get_by_test_id("stVideo").nth(0)
    expect(video_element).to_be_visible()
    # src here is a generated by streamlit url since we pass a file content
    expect(video_element).to_have_attribute("src", re.compile(r".*media.*.mp4"))


def test_video_handles_start_time(app: Page):
    video_element = app.get_by_test_id("stVideo").nth(1)
    expect(video_element).to_be_visible()
    # src here is an url we pass to st.video
    expect(video_element).to_have_attribute(
        "src", "https://www.w3schools.com/html/mov_bbb.mp4"
    )


@pytest.mark.skip_browser("chromium")
def test_handles_changes_in_start_time(
    themed_app: Page, assert_snapshot: ImageCompareFunction
):
    themed_app.wait_for_timeout(2000)
    # Change the start time of second video from 6 to 5
    themed_app.get_by_test_id("stNumberInput").locator("button.step-up").click()
    # Wait for the video start time to update
    themed_app.wait_for_timeout(2000)

    video_elements = themed_app.get_by_test_id("stVideo")
    assert_snapshot(video_elements.nth(1), name="video-updated-start")
