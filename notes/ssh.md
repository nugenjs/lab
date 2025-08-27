# SSSSSSHHHHHHHHH 🤫

## Generate keys for GitHub
``` MAC
# Look for id_ed25519 and id_ed25519.pub (or id_rsa / id_rsa.pub)
ls -al ~/.ssh 

ssh-keygen -t ed25519 -C "email used with github"

# Save to Apple Keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Copy public key to clipboard to save on GitHub
pbcopy < ~/.ssh/id_ed25519.pub
# Save it in GitHub's Settings/SSH and GPC keys

# Test it with
ssh -T git@github.com
```