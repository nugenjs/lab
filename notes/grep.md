# GREP

searches through files line by line, and returns the line if input regex pattern is found  

grep {flags} {regex pattern} {file}


### common flags
`-e`: not often used as is default. Treats `?, +, {, |, (, and )` as regular chars due to backwards compatibility.  
`-E`: extended regular expression. Treats `?, +, {, |, (, and )` as special.  
`-i`: makes pattern case insensitive.
`-F`: matches string without any regular expression.    

### examples
```
grep "^log" app.log     # search for lines
grep -E "[0-9]{3}-[0-9]{3}-[0-9]{4}" file.txt    # search for basic phone number
grep -e "warn" -e "error" file.txt    # matches warn or error. Equivalent to "warn|error"
grep -i "lowercase" UPPERCASED.txt

cat error.log | grep "throw"    # pipe from other outputs
grep "^error" *.log    # file glob
```
