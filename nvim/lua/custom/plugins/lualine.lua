return {
  'nvim-lualine/lualine.nvim',
  config = function()
    require('lualine').setup {
      dependencies = {
        'nvim-tree/nvim-web-devicons',
      },
      options = {
        theme = 'powerline',
      },
    }
  end,
}
