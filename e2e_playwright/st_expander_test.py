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

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction, wait_for_app_run
from e2e_playwright.shared.app_utils import (
    click_button,
    click_on_expander,
    expect_exception,
    get_expander,
)

EXPANDER_HEADER_IDENTIFIER = "summary"


def test_expander_displays_correctly(
    themed_app: Page, assert_snapshot: ImageCompareFunction
):
    """Test that all expanders are displayed correctly via screenshot testing."""
    expander_elements = themed_app.get_by_test_id("stExpander")
    expect(expander_elements).to_have_count(6)

    for expander in expander_elements.all():
        expect(expander.locator(EXPANDER_HEADER_IDENTIFIER)).to_be_visible()

    assert_snapshot(expander_elements.nth(0), name="st_expander-sidebar_collapsed")
    assert_snapshot(expander_elements.nth(1), name="st_expander-normal_expanded")
    assert_snapshot(expander_elements.nth(2), name="st_expander-normal_collapsed")
    assert_snapshot(expander_elements.nth(3), name="st_expander-with_input")
    assert_snapshot(expander_elements.nth(4), name="st_expander-long_expanded")
    assert_snapshot(expander_elements.nth(5), name="st_expander-long_collapsed")


def test_expander_collapses_and_expands(app: Page):
    """Test that an expander collapses and expands."""
    main_container = app.get_by_test_id("stAppViewBlockContainer")
    main_expanders = main_container.get_by_test_id("stExpander")
    expect(main_expanders).to_have_count(5)

    expanders = main_expanders.all()
    # Starts expanded
    expander_header = expanders[0].locator(EXPANDER_HEADER_IDENTIFIER)
    expect(expander_header).to_be_visible()
    toggle = expander_header.locator("svg").first
    expect(toggle).to_be_visible()
    expander_header.click()
    toggle = expander_header.locator("svg").first
    expect(toggle).to_be_visible()

    # Starts collapsed
    expander_header = expanders[1].locator(EXPANDER_HEADER_IDENTIFIER)
    expect(expander_header).to_be_visible()
    toggle = expander_header.locator("svg").first
    expect(toggle).to_be_visible()
    expander_header.click()
    toggle = expander_header.locator("svg").first
    expect(toggle).to_be_visible()


def test_empty_expander_not_rendered(app: Page):
    """Test that an empty expander is not rendered."""
    expect(app.get_by_text("Empty expander")).not_to_be_attached()


def test_expander_session_state_set(app: Page):
    """Test that session state updates are propagated to expander content"""
    main_container = app.get_by_test_id("stAppViewBlockContainer")
    main_expanders = main_container.get_by_test_id("stExpander")
    expect(main_expanders).to_have_count(5)

    # Show the Number Input
    num_input = main_expanders.nth(2).get_by_test_id("stNumberInput").locator("input")
    num_input.fill("10")
    num_input.press("Enter")
    wait_for_app_run(app)

    # Hide the Number Input
    main_expanders.nth(2).locator(EXPANDER_HEADER_IDENTIFIER).click()

    app.get_by_text("Update Num Input").click()
    wait_for_app_run(app)

    app.get_by_text("Print State Value").click()
    wait_for_app_run(app)

    text_elements = app.get_by_test_id("stText")
    expect(text_elements).to_have_count(2)

    expect(text_elements.nth(0)).to_have_text("0.0", use_inner_text=True)
    expect(text_elements.nth(1)).to_have_text("0.0", use_inner_text=True)


def test_nested_expanders_raises_exception(app: Page):
    """Test that st.expander may not be nested inside other expanders."""

    click_button(app, "Nested expander (raises exception)")
    expect_exception(
        app,
        "Expanders may not be nested inside other expanders.",
    )


def test_expandable_state(app: Page):
    """Test whether expander state is not retained for a distinct expander."""
    click_button(app, "Show expander_1")
    # Open expander_1
    click_on_expander(app, "expander_1")

    expander_1 = get_expander(app, "expander_1")
    expander_1_details = expander_1.get_by_test_id("stExpanderDetails")
    expect(expander_1_details).to_contain_text("expander_1 write")

    click_button(app, "Show expander_2")
    expect(expander_1_details).not_to_contain_text("expander_1 write")
    expect(expander_1_details).to_be_hidden()
