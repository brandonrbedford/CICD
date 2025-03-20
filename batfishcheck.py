#!/usr/bin/env python

"""Script used to test the network with Batfish."""

import os
import subprocess
import pandas as pd
from pybatfish.client.session import Session
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_incompatible_bgp_sessions,
    assert_no_incompatible_ospf_sessions,
    assert_no_unestablished_bgp_sessions,
    assert_no_undefined_references,
)
from rich.console import Console

console = Console(color_system="truecolor")


def test_duplicate_rtr_ids(snap):
    """Test for duplicate router IDs."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for duplicate "
        "router IDs[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_duplicate_router_ids(snapshot=snap, protocols=["ospf", "bgp"])
    console.print(
        ":green_heart: [bold green]No duplicate router IDs found!"
        "[/bold green] :green_heart:"
    )


def test_bgp_compatibility(snap):
    """Test for incompatible BGP sessions."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible "
        "BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_bgp_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All BGP sessions compatible!"
        "[/bold green] :green_heart:"
    )


def test_ospf_compatibility(snap):
    """Test for incompatible OSPF sessions."""
