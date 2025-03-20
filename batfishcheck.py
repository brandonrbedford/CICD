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
CONFIG_DIR = "./Snapshots"
#CLONE_DIR = "./cloned_configs"


# #def clone_repo():
#     """Clone the GitHub repository if not already cloned."""
#     if not os.path.exists(CLONE_DIR):
#         console.print(":warning: Cloning repository from GitHub...")
#         git.Repo.clone_from(GITHUB_REPO_URL, CLONE_DIR)
#     else:
#         console.print(":green_heart: Repository already cloned.")


def ensure_snapshot_directory(snapshot_dir):
    """Ensure the snapshot directory exists, cloning if necessary."""
    if not os.path.exists(snapshot_dir):
        console.print(":warning: Snapshot directory not found!")
        return False
    return True


def test_duplicate_rtr_ids(bf):
    """Test for duplicate router IDs."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for duplicate router IDs[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_duplicate_router_ids(session=bf, protocols=["ospf", "bgp"])
    console.print(
        ":green_heart: [bold green]No duplicate router IDs found![/bold green] :green_heart:"
    )


def test_bgp_compatibility(bf):
    """Test for incompatible BGP sessions."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_bgp_sessions(session=bf)
    console.print(
        ":green_heart: [bold green]All BGP sessions compatible![/bold green] :green_heart:"
    )


def test_ospf_compatibility(bf):
    """Test for incompatible OSPF sessions."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible OSPF sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_ospf_sessions(session=bf)
    console.print(
        ":green_heart: [bold green]All OSPF sessions compatible![/bold green] :green_heart:"
    )


def test_bgp_unestablished(bf):
    """Test for BGP sessions that are not established."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for unestablished BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_unestablished_bgp_sessions(session=bf)
    console.print(
        ":green_heart: [bold green]All BGP sessions are established![/bold green] :green_heart:"
    )


def test_undefined_references(bf):
    """Test for undefined references."""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for undefined references[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_undefined_references(session=bf)
    console.print(
        ":green_heart: [bold green]No undefined references found![/bold green] :green_heart:"
    )


def main():
    """Main function to run Batfish analysis on the configurations."""
    snapshot_name = "configs"  # Example snapshot name
    snapshot_dir = CONFIG_DIR

    # # Clone the GitHub repo if not already cloned
    # clone_repo()

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
    test_duplicate_rtr_ids(bf)
    test_bgp_compatibility(bf)
    test_ospf_compatibility(bf)
    test_bgp_unestablished(bf)
    test_undefined_references(bf)


if __name__ == "__main__":
    main()
