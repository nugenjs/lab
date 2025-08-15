# VIM

## Visual Mode
v or V: visual and vertical visual mode 
ctrl+v (mac): enter block visual






## Dictionary
d - delete
D - d$ delete to end of line
a - Insert mode start cursor after highlighted char
i - Insert mode start cursor at curr highlighted char







## Seach and Replace
cmd mode:
**:.,+5s/^/- /**
```
. selects current line
+4 selects next 4 select (in this case, lines)
s/^/- / regex to match start of line, and replace with "- "
```
visual mode
```
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

