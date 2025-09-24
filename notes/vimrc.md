## My current ~/.vimrc

vnoremap \y y:call system("pbcopy", getreg("\""))<CR>
nnoremap \p :call setreg("\"", system("pbpaste"))<CR>p

noremap YY "+y<CR>
noremap P "+gP<CR>
noremap XX "+x<CR>

" line number stoof
set nu rnu
" set ruler

set tabstop=2 " width of tab
set softtabstop=2 " add remove 2 whitspaces when pressing tab or backspace
set shiftwidth=2 " set indention lvl to 2 whitespaces
set expandtab " invert whitespaces instead of tab

set autoindent
" set smartindent
syntax enable
filetype plugin indent on
