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
        ":green_heart: [bold green]No duplicate router IDs found![/bold green] "
        ":green_heart:"
    )


def test_bgp_compatibility(snap):
    """Test for incompatible BGP sessions."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible "
        "BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_bgp_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All BGP sessions compatible![/bold green] "
        ":green_heart:"
    )


def test_ospf_compatibility(snap):
    """Test for incompatible OSPF sessions."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible "
        "OSPF sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_ospf_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All OSPF sessions compatible![/bold green] "
        ":green_heart:"
    )


def test_bgp_unestablished(snap):
    """Test for BGP sessions that are not established."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for unestablished "
        "BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_unestablished_bgp_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All BGP sessions are established![/bold green] "
        ":green_heart:"
    )


def test_undefined_references(snap):
    """Test for undefined references."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for undefined "
        "references[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_undefined_references(snapshot=snap)
    console.print(
        ":green_heart: [bold green]No undefined references found![/bold green] "
        ":green_heart:"
    )


def ensure_snapshot_directory(snapshot_dir):
    """Ensure the snapshot directory exists, cloning if necessary."""
    if not os.path.exists(snapshot_dir):
        console.print(
            ":warning: [bold red]Snapshot directory not found! "
            "Cloning from GitHub...[/bold red] :warning:"
        )
        subprocess.run(
            [
                "git",
                "clone",
                "--branch",
                "cisco_configs",
                "https://github.com/yourusername/yourrepo.git",
                snapshot_dir,
            ]
        )


def main():
    """Initialize the Batfish session and run network tests."""
    snapshot_name = "R1"
    snapshot_dir = "./Snapshots/"  # Ensure this path exists

    ensure_snapshot_directory(snapshot_dir)

    # Initialize Batfish session
    bf = Session(host="localhost")  # Ensure Batfish is running

    # Set network and snapshot
    bf.set_network("LAB_NETWORK")
    bf.init_snapshot(snapshot_dir, name=snapshot_name, overwrite=True)

    # Run Batfish question
    answer = bf.q.initIssues().answer()

    # Convert answer to DataFrame and print
    df = answer.frame()
    print(df)

    # RRun tests with the correct snapshot name
    test_duplicate_rtr_ids(snapshot_name)
    test_bgp_compatibility(snapshot_name)
    test_ospf_compatibility(snapshot_name)
    test_bgp_unestablished(snapshot_name)
    test_undefined_references(snapshot_name)


if __name__ == "__main__":
    main()
