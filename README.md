# dotfiles

This repository contains my personal dotfiles for various tools and applications,
including Neovim, tmux, and others. These configurations help me maintain a
consistent development environment across different machines.

The repo uses two coexisting installation mechanisms:

- **chezmoi** (`dot_*` / `executable_*` prefixed files) — copies real files
  into `$HOME` on `chezmoi apply`. Supports per-machine templating, secret
  stores, and one-command bootstrap on new machines. Used for newer additions
  (clipline, Hammerspoon, Claude skills, Ghostty, zsh fragments).
- **`install.sh`** (legacy) — creates symlinks from this repo to `$HOME` for
  the older neovim/tmux/bash entries. Kept as-is until those are migrated to
  chezmoi as well.

## Contents

### chezmoi-managed (`chezmoi apply` to install)

- `dot_local/bin/executable_clipline` — OSC 8 click-to-copy helper for shell commands
- `dot_local/bin/executable_clipline-gc` — tmpfile pruner for clipline
- `dot_hammerspoon/init.lua` — URL handler that backs clipline (`hammerspoon://copyclip`)
- `dot_config/ghostty/config` — Ghostty terminal config
- `dot_config/zsh/clean-paste.zsh` — sourced from `~/.zshrc` to add a Ctrl-X Ctrl-V clean-paste widget + background tmpfile GC
- `dot_claude/skills/clipline/SKILL.md` — Claude Code skill that teaches the model to emit `clipline` for every proposed shell command

### `install.sh` legacy (symlinked)

- `nvim/`: Neovim configuration files. Modified kickstart.nvim configuration. See [Acknowledgements](#acknowledgements) for more information.
- `.tmux.conf`: Tmux configuration file.
- `.bash_aliases`: Bash aliases.
- `install.sh`: Script to create symlinks to the config/dotfiles.
- `cursor/`: Prompts for the AI assisted development tool, [Cursor](https://cursor.com/).

## Installation (chezmoi)

```bash
brew install chezmoi
chezmoi init https://github.com/steenfuentes/dotfiles
chezmoi apply
```

On `init`, chezmoi will prompt for whether this is a work machine (the answer
is stored in `~/.config/chezmoi/chezmoi.toml` and made available to templates
as `.work`).

To pull repo changes onto an existing machine:

```bash
chezmoi update    # git pull + apply
```

To push local edits back into the repo:

```bash
chezmoi re-add <path>     # e.g., ~/.config/ghostty/config
chezmoi cd                # enter the source repo
git commit -am "..." && git push
```

## Installation (`install.sh`, legacy paths only)

## Installation

### Prerequisites

- [tmux](https://github.com/tmux/tmux)

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


