#!/usr/bin/env python

"""Script used to test the network with Batfish"""

import os
import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *
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
    """Testing for duplicate router IDs"""
    console.print(":white_exclamation_mark: [bold yellow]Testing for duplicate router IDs[/bold yellow] :white_exclamation_mark:")
    assert_no_duplicate_router_ids(snapshot=snap, protocols=["ospf", "bgp"])
    console.print(":green_heart: [bold green]No duplicate router IDs found[/bold green] :green_heart:")


def test_bgp_compatibility(snap):
    """Testing for incompatible BGP sessions"""
    console.print(":white_exclamation_mark: [bold yellow]Testing for incompatible BGP sessions[/bold yellow] :white_exclamation_mark:")
    assert_no_incompatible_bgp_sessions(snapshot=snap)
    console.print(":green_heart: [bold green]All BGP sessions compatible![/bold green] :green_heart:")


def test_ospf_compatibility(snap):
    """Testing for incompatible OSPF sessions"""
    console.print(":white_exclamation_mark: [bold yellow]Testing for incompatible OSPF sessions[/bold yellow] :white_exclamation_mark:")
    assert_no_incompatible_ospf_sessions(snapshot=snap)
    console.print(":green_heart: [bold green]All OSPF sessions compatible![/bold green] :green_heart:")


def test_bgp_unestablished(snap):
    """Testing for BGP sessions that are not established"""
    console.print(":white_exclamation_mark: [bold yellow]Testing for unestablished BGP sessions[/bold yellow] :white_exclamation_mark:")
    assert_no_unestablished_bgp_sessions(snapshot=snap)
    console.print(":green_heart: [bold green]All BGP sessions are established![/bold green] :green_heart:")


def test_undefined_references(snap):
    """Testing for any undefined references"""
    console.print(":white_exclamation_mark: [bold yellow]Testing for undefined references[/bold yellow] :white_exclamation_mark:")
    assert_no_undefined_references(snapshot=snap)
    console.print(":green_heart: [bold green]No undefined references found![/bold green] :green_heart:")


def main():
    """Initialize and test the network with Batfish."""
    SNAPSHOT_NAME = "R1"
    SNAPSHOT_DIR = "/cisco_configs/"  # Ensure this path exists

    # Verify snapshot directory exists
    if not os.path.exists(SNAPSHOT_DIR):
        console.print(f":warning: [bold red]Snapshot directory '{SNAPSHOT_DIR}' does not exist![/bold red] :warning:")
        return

    # Initialize Batfish session
    bf = Session(host="localhost")  # Ensure Batfish is running

    # Set network and snapshot
    bf.set_network("LAB_NETWORK")
    bf.init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)

    # Run Batfish question
    answer = bf.q.initIssues().answer()

    # Convert answer to DataFrame and print
    df = answer.frame()
    print(df)

    # Run tests with the correct snapshot name
    test_duplicate_rtr_ids(SNAPSHOT_NAME)
    test_bgp_compatibility(SNAPSHOT_NAME)
    test_ospf_compatibility(SNAPSHOT_NAME)
    test_bgp_unestablished(SNAPSHOT_NAME)
    test_undefined_references(SNAPSHOT_NAME)


if __name__ == "__main__":
    main()


# #!/usr/bin/env python
#
# """Script used to test the network with batfish"""
#
# import pandas as pd
# from pybatfish.client.session import Session
# from pybatfish.datamodel import *
# from pybatfish.datamodel.answer import *
# from pybatfish.datamodel.flow import *
#
# #from pybatfish.client.commands import *
# #from pybatfish.question import load_questions
# from pybatfish.client.asserts import (
#     assert_no_duplicate_router_ids,
#     assert_no_incompatible_bgp_sessions,
#     assert_no_incompatible_ospf_sessions,
#     assert_no_unestablished_bgp_sessions,
#     assert_no_undefined_references,
# )
# from rich.console import Console
#
#
# console = Console(color_system="truecolor")
#
#
# def test_duplicate_rtr_ids(snap):
#     """Testing for duplicate router IDs"""
#     console.print(
#         ":white_exclamation_mark: [bold yellow]Testing for duplicate router IDs[/bold yellow] :white_exclamation_mark:"
#     )
#     assert_no_duplicate_router_ids(
#         snapshot=snap,
#         protocols=["ospf,bgp"],
#     )
#     console.print(
#         ":green_heart: [bold green]No duplicate router IDs found[/bold green] :green_heart:"
#     )
#
#
# def test_bgp_compatibility(snap):
#     """Testing for incompatible BGP sessions"""
#     console.print(
#         ":white_exclamation_mark: [bold yellow]Testing for incompatible BGP sessions[/bold yellow] :white_exclamation_mark:"
#     )
#     assert_no_incompatible_bgp_sessions(
#         snapshot=snap,
#     )
#     console.print(
#         ":green_heart: [bold green]All BGP sessions compatible![/bold green] :green_heart:"
#     )
#
#
# def test_ospf_compatibility(snap):
#     """Testing for incompatible OSPF sessions"""
#     console.print(
#         ":white_exclamation_mark: [bold yellow]Testing for incompatible OSPF sessions[/bold yellow] :white_exclamation_mark:"
#     )
#     assert_no_incompatible_ospf_sessions(
#         snapshot=snap,
#     )
#     console.print(
#         ":green_heart: [bold green]All OSPF sessions compatible![/bold green] :green_heart:"
#     )
#
#
# def test_bgp_unestablished(snap):
#     """Testing for BGP sessions that are not established"""
#     console.print(
#         ":white_exclamation_mark: [bold yellow]Testing for unestablished BGP sessions[/bold yellow] :white_exclamation_mark:"
#     )
#     assert_no_unestablished_bgp_sessions(
#         snapshot=snap,
#     )
#     console.print(
#         ":green_heart: [bold green]All BGP sessions are established![/bold green] :green_heart:"
#     )
#
#
# def test_undefined_references(snap):
#     """Testing for any undefined references"""
#     console.print(
#         ":white_exclamation_mark: [bold yellow]Testing for undefined references[/bold yellow] :white_exclamation_mark:"
#     )
#     assert_no_undefined_references(
#         snapshot=snap,
#     )
#     console.print(
#         ":green_heart: [bold green]No undefined refences found![/bold green] :green_heart:"
#     )
#
#
# def main():
#     """init all the things"""
#     #NETWORK_NAME = "LAB_NETWORK"
#     SNAPSHOT_NAME = "R1"
#     SNAPSHOT_DIR = "./cisco_configs/"
#    # bf_session.host = "192.168.219.128"
#     bf = Session(host="localhost")
#     bf.set_network('LAB_NETWORK')
#     init_snap = bf.init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)
#     #load_questions()
#     answer = bf.q.initIssues().answer()
#     # Convert the answer to a Pandas DataFrame
#     df = answer.frame()
#     test_duplicate_rtr_ids(SNAPSHOT_NAME)
#     test_bgp_compatibility(SNAPSHOT_NAME)
#     test_ospf_compatibility(SNAPSHOT_NAME)
#     test_bgp_unestablished(SNAPSHOT_NAME)
#     test_undefined_references(SNAPSHOT_NAME)
#
#
# if __name__ == "__main__":
#     main()
