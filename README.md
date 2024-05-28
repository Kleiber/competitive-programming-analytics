# Competitive Programming Analytics (CPA)

Competitive Programming Analytics (CPA) is a tool to help with competitive programming development.

## Overview
`cpa` is a command line that aims to help competitive programmers optimizing code compilation, testing, and debugging time.

## Installing

Using `cpa` command line is simple. First, clone the repository in your workspace

```bash
cd $HOME
git clone https://github.com/Kleiber/cpa.git
cd cpa
pyhton3 install -r requirements.txt
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
