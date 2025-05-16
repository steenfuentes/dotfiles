#! /bin/bash

# Intended to setup a suite of core dependencies to contribute within the 
# AI and Advanced Analytics team at Avidity. This script installs system level
# tools and dependencies and language-related tools. It is not intended to install
# python packages or node packages. It is assumed that the user has already
# installed the language runtimes (python, node, etc.). If not, see the README
# for instructions on how to install the language runtimes.

# Get the OS type from the input arguments (only macos currently supported. Any
# other OS string will be returned as unsupported)
OS_TYPE=$1

# Install the tools
install_tools() {
    case $OS_TYPE in
        macos)
            install_macos_tools
            ;;
        *)
            echo "Unsupported OS type: $OS_TYPE"
    esac
}

# Install the tools for macos
install_macos_tools() {
    # Install Homebrew
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew already installed"
    fi

    # Install tools
    brew update
    brew install azure-cli

    brew tap azure/functions
    brew install azure-functions-core-tools@4

    brew install dotnet
    brew install duckdb
    brew install git
    brew install gh
    brew install parquet-cli
    brew install pyenv
    brew install pyenv-virtualenv
    brew install node@20
}

# Install the tools for linux
install_ubuntu_tools() {
    echo "Unfortunately, this script does not support 
}
