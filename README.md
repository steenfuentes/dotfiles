# dotfiles

This repository contains my personal dotfiles for various tools and applications,
including Neovim, tmux, and others. These configurations help me maintain a
consistent development environment across different machines.

Files and directories are symlinked to their appropriate locations on the 
local machine. Use the `install.sh` script to create the symlinks. Details
in the [Installation](#installation) section.

## Installation

To install the dotfiles, clone this repository to your local machine and run
the `install.sh` script. The script will create symlinks to the dotfiles in
the appropriate locations.

1. Clone the repository to your local machine:

```bash
git clone https://github.com/steenfuentes/dotfiles.git {YOUR_DOTFILES_DIR}
```

2. Change to the dotfiles directory:

```bash
cd {YOUR_DOTFILES_DIR}
```

3. Make the `install.sh` script executable:

```bash
chmod +x install.sh
```

4. Run the `install.sh` script:

```bash
./install.sh
```

5. Restart your terminal or source the appropriate files to apply the changes.

```bash
source ~/.bashrc
```

## Acknowledgements

```nvim``` configuration is a personalize version of the ```kickstart.nvim``` found on github: [nvim-lua/kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim)
```tmux``` configuration inspired by [typecraft-dev](https://github.com/typecraft-dev)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


