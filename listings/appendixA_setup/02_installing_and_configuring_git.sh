# Windows: download the installer from git-scm.com
# macOS:   xcode-select --install     (or: brew install git)
# Ubuntu:  sudo apt install git

git config --global user.name "Your Name"
git config --global user.email "you@university.edu"
git config --global init.defaultBranch main

# Create an SSH key and add the public key to GitHub (Settings > SSH keys)
ssh-keygen -t ed25519 -C "you@university.edu"
cat ~/.ssh/id_ed25519.pub
ssh -T git@github.com                # test the connection
