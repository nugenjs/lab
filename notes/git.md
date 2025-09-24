# GIT GUD


## Commonly Used
`git reset .`: opposite of add. This removes all from staging. Can specify files or use patterns.\
`git rm --cached filename`: remove files from git. (e.g. `git rm --cached **/.DS_STORE`)\
`git update-index --assume-unchanged dir/changeme.txt`: git will ignore changes to this file\
`git stash push -u -m 'Stash message'`: common stash command to include untracked\
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

## GitIgnore
`/name`: Start with `/` to ignore in current directory\
`name`: Ignores in subdirectories

## Stash
Copy stash from repo1 to repo2:\
repo 1: `git stash show -up stash@{0} > /tmp/stash.patch`, repo 2: `git apply /tmp/stash.patch`.
