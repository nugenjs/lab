# GIT GUD


## Init existing directory
```
git init
git add .
git commit -m 'message here'
git remote add origin <url of repository>
git push -u origin main
```

## Defs
`git reset .`: opposite of add. This removes all from staging. Can specify files or use patterns.
`git rm --cached filename`: remove files from git. (e.g. `git rm --cached **/.DS_STORE`)

## General Notes
Create .gitignore before initial commit. Avoids adding node_modules to git.
