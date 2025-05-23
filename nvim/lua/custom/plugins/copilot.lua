return {
  'github/copilot.vim',
  config = function()
    vim.keymap.set('i', '<C-c><C-a>', 'copilot#Accept("")', {
      expr = true,
      replace_keycodes = false,
    })
    vim.g.copilot_no_tab_map = true
    github_copilot = require 'copilot'
  end,
}
