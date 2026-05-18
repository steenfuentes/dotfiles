---
name: clipline
description: >
  Render every shell command Claude proposes for the user to run as a clickable
  OSC 8 hyperlink in the Ghostty terminal via the `clipline` helper. Cmd-clicking
  the link copies the exact, unmangled command string to the macOS clipboard
  (no terminal line-wrap damage, ANSI escapes, or pseudo-graphics). Triggers
  whenever the assistant is about to output a shell command, bash one-liner,
  multi-line script, CLI invocation, npm/uv/git/brew/gh command, curl, or any
  string the user would copy-paste into another terminal. Applies in any
  Claude Code session running inside Ghostty on this machine. Skip when the
  command is being executed by Claude itself in the same turn (internal Bash
  tool calls don't need clipline) — only commands intended for the user to run
  manually.
---

# clipline

Every shell command proposed **for the user to run manually** must be emitted
through the `clipline` helper so it renders as a clickable copy-link in Ghostty.

## When to use

**Use clipline when:**
- Telling the user to run a command in their own shell
- Proposing setup, install, or debug commands
- Suggesting a sequence of commands — emit one `clipline` per command
- Any command shown in a response with the intent "run this"

**Skip clipline when:**
- Claude is about to run the command itself via the Bash tool in the same turn
- The command is illustrative only (referenced in prose, not meant to be executed)
- The user is in a non-Ghostty environment (rare; default to using it)

## How

Invoke via the Bash tool. One call per command:

```
clipline 'THE_COMMAND_TEXT'
```

The helper writes the payload to `/tmp/clipline-<sha1>.txt`, prints an OSC 8
hyperlink to stdout pointing at `hammerspoon://copyclip?id=<sha1>`, and the
user Cmd-clicks to copy. Truncates the visible label to 80 chars; full text
goes to the clipboard.

### Quoting rules

- **Single-quote** the argument to `clipline`.
- **Literal single quotes** inside the command: escape as `'\''`.
- **Multi-line commands**: pass a single-quoted argument with literal newlines.
  `clipline` preserves the full text in the clipboard; the visible label
  collapses newlines to `⏎`.
- **Double quotes, backticks, `$`, `!`** inside single quotes pass through
  literally — no escaping needed.

### Examples

Single command:
```
clipline 'brew install --cask hammerspoon'
```

Command with double quotes + pipes:
```
clipline 'echo "hello world" | grep -o hello'
```

Command with embedded single quotes (escape as `'\''`):
```
clipline 'find . -name '\''*.py'\'' -exec wc -l {} +'
```

Multi-line command:
```
clipline 'set -e
cd ~/project
npm install
npm run build'
```

Multiple commands in one response — one `clipline` per command, each becomes
its own clickable line:
```
clipline 'brew install gh'
clipline 'gh auth login'
clipline 'gh repo clone myorg/myrepo'
```

## Output flow

1. Explain what each command does in prose.
2. Emit `clipline '...'` via Bash tool.
3. The Bash tool result contains the OSC 8 escape sequence + visible label.
4. Ghostty renders the line as a clickable `📋 <label>` hyperlink.
5. User Cmd-clicks → Hammerspoon URL handler reads the tmpfile → `pbcopy`.

## Failure modes the user may report

| Symptom | Cause | Fix |
|---|---|---|
| Line not clickable | User didn't hold Cmd | Cmd-click, not plain click |
| `📋 copied` flashes but clipboard empty | Tmpfile pruned (>24h) | Re-emit via clipline |
| Click does nothing, no flash | Hammerspoon not running | `open -a Hammerspoon` |
| Escape sequences shown as literal text | Terminal not Ghostty, or tmux without `terminal-features ',*:hyperlinks'` | Use Ghostty natively; or add tmux setting |
| Permission prompt every call | `Bash(clipline:*)` not allowlisted | Check `~/.claude/settings.json` |

## Backing pieces (reference)

- Helper: `~/.local/bin/clipline` (bash script; sha1 + tmpfile + OSC 8 emit)
- GC: `~/.local/bin/clipline-gc` (prunes tmpfiles >24h, fires at zsh start)
- URL handler: `~/.hammerspoon/init.lua` (reads tmpfile, `hs.pasteboard.setContents`)
- Permission: `~/.claude/settings.json` → `permissions.allow: ["Bash(clipline:*)"]`
- Fallback for unrendered output: `Ctrl-X Ctrl-V` zsh widget in `~/.zshrc`
  (`clean_paste` strips ANSI + gutter chars from `pbpaste`)

## Do NOT

- Do not invoke `clipline` on commands you are running yourself in the same
  turn (would spam tmpfiles for no benefit).
- Do not wrap a `clipline` call inside another `clipline` call.
- Do not pass shell-substitution payloads (`$(...)`, backticks) expecting them
  to interpolate — `clipline` treats the argument as literal text. If you want
  the user's clipboard to contain `$(date)`, write it literally inside the
  single-quoted argument.
- Do not emit `clipline` lines in prose/markdown blocks — they must be **actual
  Bash tool invocations** so the OSC 8 escape sequence reaches the terminal.
