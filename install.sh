#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to create symlink
create_symlink() {
    if [ -e "$2" ]; then
        echo -e "${YELLOW}WARNING: $2 already exists. Skipping...${NC}"
    else
        ln -s "$1" "$2"
        echo -e "${GREEN}Created symlink: $2 -> $1${NC}"
    fi
}

# Create symlinks
echo "Creating symlinks..."
create_symlink "$PWD/nvim" "$HOME/.config/nvim"
create_symlink "$PWD/.tmux.conf" "$HOME/.tmux.conf"
create_symlink "$PWD/.bash_aliases" "$HOME/.bash_aliases"

# Check and modify .bashrc
echo "Checking .bashrc..."
if grep -q "# Bash Aliases" "$HOME/.bashrc"; then
    echo -e "${GREEN}Bash Aliases section already exists in .bashrc${NC}"
else
    echo "Adding Bash Aliases section to .bashrc"
    echo "" >> "$HOME/.bashrc"
    echo "# Bash Aliases" >> "$HOME/.bashrc"
    echo "if [ -f ~/.bash_aliases ]; then" >> "$HOME/.bashrc"
    echo "    . ~/.bash_aliases" >> "$HOME/.bashrc"
    echo "fi" >> "$HOME/.bashrc"
    echo -e "${GREEN}Added Bash Aliases section to .bashrc${NC}"
fi

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}NOTE: You may need to restart your terminal or run 'source ~/.bashrc' for changes to take effect.${NC}"
