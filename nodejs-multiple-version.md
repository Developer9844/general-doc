
Create a .nvmrc File: In your project directory, create a .nvmrc file with the desired Node.js version:
```
echo"18.16.0" > .nvmrc
```

Add the Following Snippet to Your .bashrc
```
# Automatically switch Node versions using .nvmrc in Bash
load-nvmrc() {
  if [[ -f .nvmrc ]]; then
    local nvmrc_node_version
    nvmrc_node_version=$(<.nvmrc)

    # If the current Node version is not the one specified in the .nvmrc, switch to it
    if [[ $(nvm current) != "v${nvmrc_node_version}" ]]; then
      nvm use
    fi
  elif [[ $(nvm current) != "$(nvm version default)" ]]; then
    # If no .nvmrc file is found, revert to the default Node version
    echo "Reverting to nvm default version"
    nvm use default
  fi
}

# Hook the function to the 'cd' command
cd() {
  builtin cd "$@" && load-nvmrc
}

# Run once to handle the current directory
load-nvmrc
```


# Global Configuration

curl -o- https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash

sudo mkdir -p /usr/local/nvm
sudo curl -o- https://raw.githubusercontent.com/creationix/nvm/master/install.sh | NVM_DIR=/usr/local/nvm bash


sudo tee /etc/profile.d/nvm.sh <<'EOF'
export NVM_DIR="/usr/local/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
EOF


sudo chmod +x /etc/profile.d/nvm.sh


source /etc/profile.d/nvm.sh

echo 'source /etc/profile.d/nvm.sh' >> ~/.bashrc




~/.bashrc:

export NVM_DIR="/usr/local/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"


source ~/.bashrc
```
source ~/.bashrc
```

