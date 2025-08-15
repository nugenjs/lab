# zshrc MAC config
### File can be loaded as is into ~/.zshrc

## Javscript
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

## Environment Variables
BASE_URL='172.28.98.222'

## Aliases
alias python=python3
alias pip=pip3
alias py=python
alias sauce="source ~/.zshrc"
alias zrc="code -r ~/.zshrc"
alias zrv="vim ~/.zshrc"

## Shell Functions
function killport() {
  if [[ -z "$1" ]]; then
    echo "Usage: killport <port>"
    return 1
  fi

  local port=$1
  local pid

  pid=$(lsof -ti tcp:$port)

  if [[ -z "$pid" ]]; then
    echo "No process found running on port $port"
    return 0
  fi

  echo "Killing process $pid running on port $port..."
  kill -9 $pid && echo "Process $pid killed."
}




## GAI Stuff
alias lma=ollama


## Closing
echo "sauced"
