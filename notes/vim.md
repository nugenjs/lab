# VIM

## Dictionary
`d` - delete\
`D` - d$ delete to end of line\
`a` - Insert mode start cursor after highlighted char\
`i` - Insert mode start cursor at curr highlighted char

## Visual Mode
Selecting char(s) with highlight\
`v or V`: visual and vertical visual mode\
`ctrl+v (mac)`: enter line  visual

### example usage
`v` to enter visual mode. Highlight text you want to copy. y to yank. Move cursor to where you want to paste. `p` to paste copied text.\
`Shift + v` visual line mode. Highlight test to copy to clipboard. Type `:` will auto fill `:'<,'>`. Set command to `:'<,'>w !clip.exe`





## Search and Replace
`/` and type word\
`n` next found\
`N` prev found 


### example usage
```
/hello world    # find next "hello world"


Search for lines that start with "- "  
  cmd mode:
  **:.,+5s/^/- /**
  . selects current line
  +4 selects next 4 select (in this case, lines)
  s/^/- / regex to match start of line, and replace with "- "

  visual mode
  vertical visual mode, go down 4 lines to select 5 lines total
  :'<,,'> will automatically fill
  :'<,,'>s/^/- / 
```




## Config
relative line number
:set rnu    " toggle relative numbering on
:set rnu!    " toggle relative numbering off
hybrid relative
:set nu rnu

