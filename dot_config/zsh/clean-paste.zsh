# Source from ~/.zshrc:
#   [[ -f ~/.config/zsh/clean-paste.zsh ]] && source ~/.config/zsh/clean-paste.zsh
#
# Provides:
#   - clean_paste: strip ANSI + Unicode box-drawing + gutter chars from pbpaste
#   - Ctrl-X Ctrl-V: insert cleaned clipboard contents at the prompt
#   - Background tmpfile GC at shell start (prunes /tmp/clipline-*.txt >24h)

clean_paste() {
  pbpaste \
    | perl -pe 's/\e\[[0-9;?]*[a-zA-Z]//g' \
    | perl -CSD -pe 's/[\x{2500}-\x{257F}\x{2580}-\x{259F}]//g' \
    | tr -d '\r' \
    | sed 's/^[[:space:]]*│[[:space:]]*//' \
    | sed 's/[[:space:]]*$//'
}
clean-paste-widget() { LBUFFER+="$(clean_paste)"; }
zle -N clean-paste-widget
bindkey '^X^V' clean-paste-widget

( ~/.local/bin/clipline-gc & ) >/dev/null 2>&1
