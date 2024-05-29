# Competitive Programming Analytics (CPA)

## Overview

Competitive Programming Analytics (CPA) is a tool to help with competitive programming development.

## Installing

Using `cpa` command line is simple. First, clone the repository in your workspace

```bash
cd $HOME
git clone https://github.com/Kleiber/cpa.git
cd cpa
pip3 install -r requirements.txt
```

If we use `Ubuntu` and we had the following error when installing the requeriments `externally-managed-environment`. This is a workaround, create the virtual environment to install them.

```bash
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
```

### Linux

Next, include the following line in your `.bashrc` file (use the command `vim ~/.bashrc` to edit)

```bash
export PATH=$PATH:$HOME/cpa:
```

Finally, restart your terminal or run the command `source ~/.bashrc`

### Mac
For Mac, clone the repository in your workspace and include the following line in your `.zshrc` file (use the command `vim ~/.zshrc` to edit)

```bash
export PATH=$PATH:$HOME/cpa:
```

Finally, restart your terminal or run the command `source ~/.zshrc`

## Run

To start the server simply run the following command in a terminal tab

```bash
cpa
```

Then open the following link in the browser http://127.0.0.1:8050/
