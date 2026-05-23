# tools/dev-docs/UBUNTU.md

Document the commands used to create a dev environment on Ubuntu

## ============= Step 1. Setup Dev Environment
sudo mkdir -p /opt/dev
sudo chown -R mike:mike /opt/dev
cd /opt/dev


## ============= Step xx. Setup SSH Keys
ssh-keygen -t ed25519 -C "mike@oscar-github"
ls ~/.ssh
cat ~/.ssh/id_ed25519.pub

## ============= Step xx. Add keys to GitHub
  1. Go to GitHub
  2. Click your profile picture → Settings
  3. Click SSH and GPG keys
  4. Click New SSH key
  5. Name it something like:
    oscar-ubuntu-build-server
  6. Paste the key
  7. Save

## ============= Step xx. Test connection
ssh -T git@github.com

You should see:
Hi devmukmuk! You've successfully authenticated...

## ============= Step xx. Clone repo
git clone git@github.com:devmukmuk/CodeIt.git

## ============= Install/Update Python


## ============= Step xx. Create/activate project .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller

## ============= Step xx. Modify tools/build.py


## ============= Step xx. Make it executable
chmod +x tools/build.py

## ============= Step xx. View permissions
ls -l tools/build.py

You should see:
-rwxr-xr-x

## ============= Step xx. Run cross-platform build script
python3 -m tools.build


Author: Mike Mattinson
Updated: Feb/23/2026