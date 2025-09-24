# GNU


## quotes
Single vs double quotes. Single quotes don't example variables, but double quotes do.  
```
echo '$NODE_ENV`  # $NODE_ENV
echo "$NODE_ENV"  # development
echo "$(cat helloworld.txt)"  # hello world
  ```


## Commands
`chmod +x`: makes a file or directory executable (e.g. ./filename)    
`mv filename newfilename`: renames/moves a file  
`mv directory newdirectoryname`: renames/moves directory  
`mv directory/* newdirectoryname`: renames/moves files inside directory  
`cp filename newfilename`: copies a file  
`cp -R directory newdirectoryname`: copies directory  
`rm filename`: removes file (only unlinks, data still exists)  
`rmdir directory`: removes a directory  

## xargs
Takes output from one command and uses it as input for another command.\
`-I`: replaces occurances with following string. (e.g. `-I{abc echo {abc`)

Find all repos with pattern "cloned*" and get branch name (when working on multiple branches at the same time):\
`ls -d *cloned* | xargs -I {} git -C {} rev-parse --abbrev-ref HEAD`