import os
#import git
from pybatfish.client.session import Session
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_incompatible_bgp_sessions,
    assert_no_incompatible_ospf_sessions,
    assert_no_unestablished_bgp_sessions,
    assert_no_undefined_references,
)
from rich.console import Console

# Initialize console for better output formatting
console = Console(color_system="truecolor")

# Define constants
GITHUB_REPO_URL = "https://github.com/brandonrbedford/cicd.git"
REPO_NAME = "cicd"  # Replace with your actual repo name
CONFIG_DIR = "Snapshots/configs"
CLONE_DIR = "./cloned_configs"


def clone_repo():
    """Clone the GitHub repository if not already cloned."""
    if not os.path.exists(CLONE_DIR):
        console.print(":warning: Cloning repository from GitHub...")
        git.Repo.clone_from(GITHUB_REPO_URL, CLONE_DIR)
    else:
        console.print(":green_heart: Repository already cloned.")


def ensure_snapshot_directory(snapshot_dir):
    """Ensure the snapshot directory exists, cloning if necessary."""
    if not os.path.exists(snapshot_dir):
        console.print(":warning: Snapshot directory not found!")
        return False
    return True


def test_duplicate_rtr_ids(snap):
    """Test for duplicate router IDs."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for duplicate router IDs[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_duplicate_router_ids(snapshot=snap, protocols=["ospf", "bgp"])
    console.print(
        ":green_heart: [bold green]No duplicate router IDs found![/bold green] :green_heart:"
    )


def test_bgp_compatibility(snap):
    """Test for incompatible BGP sessions."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_bgp_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All BGP sessions compatible![/bold green] :green_heart:"
    )


def test_ospf_compatibility(snap):
    """Test for incompatible OSPF sessions."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible OSPF sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_ospf_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All OSPF sessions compatible![/bold green] :green_heart:"
    )


def test_bgp_unestablished(snap):
    """Test for BGP sessions that are not established."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for unestablished BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_unestablished_bgp_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All BGP sessions are established![/bold green] :green_heart:"
    )


def test_undefined_references(snap):
    """Test for undefined references."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for undefined references[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_undefined_references(snapshot=snap)
    console.print(
        ":green_heart: [bold green]No undefined references found![/bold green] :green_heart:"
    )


def main():
    """Main function to run Batfish analysis on the configurations."""
    snapshot_name = "snapshot_01"  # Example snapshot name
    snapshot_dir = os.path.join(CLONE_DIR, CONFIG_DIR)

    # Clone the GitHub repo if not already cloned
    clone_repo()

    # Ensure the snapshot directory exists
    if not ensure_snapshot_directory(snapshot_dir):
        console.print(":red_heart: Exiting due to missing snapshot directory.")
        return

    # Initialize Batfish session
    bf = Session(host="192.168.219.128")  # Ensure Batfish is running

    # Set network and snapshot in Batfish
    bf.set_network("LAB_NETWORK")
    bf.init_snapshot(snapshot_dir, name=snapshot_name, overwrite=True)

    # Run Batfish question (example for issues)
    answer = bf.q.initIssues().answer()

    # Convert answer to DataFrame and print
    df = answer.frame()
    print(df)

    # Run common tests on the configurations
    test_duplicate_rtr_ids(snapshot_name)
    test_bgp_compatibility(snapshot_name)
    test_ospf_compatibility(snapshot_name)
    test_bgp_unestablished(snapshot_name)
    test_undefined_references(snapshot_name)


if __name__ == "__main__":
    main()
