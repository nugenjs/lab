# GIT GUD


## Commonly Used
`git reset .`: opposite of add. This removes all from staging. Can specify files or use patterns.  
`git rm --cached filename`: remove files from git. (e.g. `git rm --cached **/.DS_STORE`)  
`git stash push -u -m 'Stash message'`: common stash command to include untracked  
`git stash apply 0`: apply latest stash

## Init existing directory
```
git init
git add .
git commit -m 'message here'
git remote add origin <url of repository>
git push -u origin main
```

## General Notes
Create .gitignore before initial commit. Avoids adding node_modules to git.  
