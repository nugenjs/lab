# Unix things


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

