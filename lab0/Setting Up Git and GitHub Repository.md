# CSCI 3212 Lab 0
Guide by [AmCh-Q](https://github.com/AmCh-Q) on GitHub.

This is a more in-depth guide compared to ``Git in one minute`` from ``index.md`` focusing more on GitHub and SSH authentication.
This guide is slightly Windows-focused, if you use a Mac/Linux you can feed this to an LLM for a guide.

## Goals
1. Install Git.
2. Create your own GitHub account and code repository.
3. Create your own ssh key and connect it to GitHub.
4. Learn how to use some Git commands, without using the web interface or desktop apps.

If you have learned these before, just do the following:
1. Fork and clone this GitHub repository: https://github.com/Zirikly-teaching/algorithms-labs-gw26
2. Within it, find the folder ``lab0`` and write your Python scripts.

## Install Git
You need this to learn how to maintain a code repository, a place where you will store your classworks.
1. Download and install from here: https://git-scm.com/install/
2. Open git bash and verify successful installation by running this command:
```bash
git --version
```
You should see something like "git version 2.55.0" -- The exact version don't matter.

## Create your GitHub account

If you don't have a GitHub account yet, create one now: https://github.com/signup.

You don't have to use your school email, but we will assume you used your school email moving forward.

## Generate your own SSH key
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/  
ssh keys are one way other people verify your identity, and we will use it so GitHub knows who you are.

Open Git bash run this to generate your ssh key:
```bash
ssh-keygen -t ed25519 -C "Write some comment here such as your email."
```
It will ask you to create a password. Then you should see ``id_ed25519`` and ``id_ed25519.pub`` at ``C:\Users\YourUserName\.ssh`` if you are using Windows.  
If you can't find it, see https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys

## Upload your SSH public key to GitHub

An SSH key has two parts:  
``id_ed25519``(with no suffix) is your private secret - **DO NOT give it to ANYONE**.  
If you read something like ``-----BEGIN OPENSSH PRIVATE KEY-----`` **STOP**.  
``id_ed25519.pub`` is your public key - you will upload it to GitHub:

1. Log into GitHub
2. Open https://github.com/settings/ssh/new
3. Give it a title, then copy the content of your ``id_ed25519.pub`` to the "Key" window. It should begin with something like ``ssh-ed25519``.
4. Click "add .ssh key"

Once you have done that, try:
```bash
ssh -T git@github.com
```
It might ask you to confirm, enter ``yes``.  
If it tells you ``You've successfully authenticated, but GitHub does not provide shell access.`` then success! GitHub can now recognize you from your ssh key.  

## Fork the class GitHub and clone it to your computer
1. Open our class' GitHub repository: https://github.com/Zirikly-teaching/algorithms-labs-gw26
2. On the top right, find the button "Fork", click it and follow the prompts to create your own copy of the class repository where you can write however you like.
3. Your forked repository is now at https://github.com/YourUserName/algorithms-labs-gw26, clone it to your local computer:
```bash
git clone git@github.com:YourUserName/algorithms-labs-gw26.git
cd algorithms-labs-gw26
```
You can use this to store your class projects and assignment submissions.

**DO NOT** clone ``Zirikly-teaching/algorithms-labs-gw26.git``! That is the class official repository and you won't have access to push changes into it later. Clone your own fork.  

## Set your own identity

```bash
git config --local user.name "Your Full Name or GitHub username"
git config --local user.email "YourGitHubUserName@users.noreply.github.com"
```
This is so that your commits later knows who you are.

## Add upstream

```bash
# Sets the class repository as the "upstream"
git remote add upstream git@github.com:Zirikly-teaching/algorithms-labs-gw26.git
# Verify
git remote -v
```
So you can do this later:
```bash
# If the class repository (upstream) changes
# you will use these commands to sync the updates to your repository.
git fetch upstream
git merge upstream/main
```

## Write something
```bash
cd lab0
```
Within ``lab0`` Write whatever you want, but know that **other people can see it** later.  
You might want to use this opportunity to create your first python scripts.  

## Commit it
```bash
git add -A
git commit -m "Initial Commit"
```
The first line stages all of your newly create files (prepares them to be committed).  
The second line commits them, as well as all modifications if you have any, and gives the commit a comment.  
This might feel tedious, but this is necessary for large group projects - each person make their own changes and periodically make a single, bulk commit, so that a team can more effectively track each person's contributions. This also allows us to easily see your work progress.  

## Push your local changes back to your GitHub
```bash
git push origin main
```
Once your have done that, refresh your page https://github.com/YourUserName/algorithms-labs-gw26/, and you should see your GitHub repository reflecting your new changes.

## You are done with the setup!

In the future, you can:

0. At anytime, run this to check the status
```bash
git status
```
1. Use the following to sync your repository to the class repository.
```bash
# Ensure you have committed your work before merging upstream changes
git fetch upstream
git merge upstream/main
```
2. make any file edits inside your ``algorithms-labs-gw26`` folder
3. commit your changes and push them to GitHub:
```bash
git add -A
git commit -m "Your commit message"
git push origin main
``` 
Try making some changes then push again.  

## Useful resources:
1. Git Cheat Sheet: https://git-scm.com/cheat-sheet
2. gitignore: https://git-scm.com/docs/gitignore. This tells git to ignore some files, useful to avoid accidentally pushing junk or sensitive files - your GitHub repository is public, anyone can read your commits.