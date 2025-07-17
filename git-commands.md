1. git init: Initializes a new Git repository in the current directory.
2. git clone <repository_url>: Creates a copy of a remote Git repository on your local machine.
3. git add <file>: Stages changes in a file for the next commit.
4. git add . or git add --all: Stages all changes in the current directory for the next commit.
5. git commit -m "commit message": Records the staged changes in a commit with a descriptive message.
6. git status: Shows the status of your working directory, including changes and untracked files.
7. git log: Displays a chronological list of all commits in the repository.
8. git branch: Lists all branches in the repository and shows the current branch.
9. git checkout <branch>: Switches to a different branch.
10. git checkout -b <new_branch>: Creates a new branch and switches to it.
11. git merge <branch>: Merges changes from one branch into the current branch.
12. git pull: Fetches changes from a remote repository and merges them into the current branch.
13. git push: Pushes local commits to a remote repository.
14. git remote -v: Lists the remote repositories associated with your local repository.
15. git fetch: Fetches changes from a remote repository without merging.
16. git reset <file>: Unstages changes in a file.
17. git reset --hard <commit>: Resets the repository to a specific commit, discarding all changes after that commit.
18. git diff: Shows the differences between the working directory and the last commit.
19. git stash: Temporarily saves changes in a "stash" to work on something else.
20. git tag <tag_name>: Creates a lightweight tag to mark a specific commit.
21. git remote add <name> <url>: Adds a new remote repository to your Git configuration.
22. git remote remove <name>: Removes a remote repository from your Git configuration.
23. git rm <file>: Removes a file from both the working directory and Git.
24. git revert <commit>: Creates a new commit that undoes the changes introduced by a previous commit.
25. git blame <file>: Shows the commit history and authorship of each line in a file.



If you've mistakenly pulled the wrong branch into your local repository and you want to undo this operation and get back to your "stage" branch, you can follow these steps:

1. Check the Current State:
   First, check the status of your local repository using the git status command. This will show you if there are any uncommitted changes in your current branch.
2. Undo the Pull Operation:
   If you've pulled the "develop" branch and want to revert it, you can use the git reset and git checkout commands. Assuming you have no uncommitted changes, you can do the following:
```
git reset --hard HEAD~1
git checkout stage
```

- The git reset --hard HEAD~1 command will reset your current branch to the previous state, effectively undoing the pull operation.
- The git checkout stage command will switch to your "stage" branch.






```
git status
On branch stage
Your branch is up to date with 'origin/stage'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        public/cmsImage/Nadia+Keynote-52.jpg_1693910682499.jpg
        public/cmsImage/Porsche-992-911-Exterior-154388.jpg_1693909629945.jpg
```

It looks like you have untracked files in your local repository after undoing the pull operation from the "develop" branch. To revert these changes and get back to the state of your "stage" branch, you can do the following:

Stash Your Untracked Files (Optional):

If you want to keep these untracked files but not commit them, you can stash them for later use. Use the following command:
```
git stash
```

This will save your untracked files in a temporary stash, allowing you to work on them later.

1. Checkout the "stage" Branch:
   Make sure you're on the "stage" branch:
```
git checkout stage
```

1. Remove Untracked Files:
   If you want to completely remove these untracked files from your working directory, you can use the git clean command with the -f and -d options:
```
git clean -f -d
```

This will remove all untracked files and directories in your working directory. Be very cautious with this command, as it will permanently delete these files.

1. Apply Stash (If Stashed):
   If you stashed your untracked files earlier and want to apply them, you can use:
```
git stash pop
```

This will apply the most recent stash. If you have multiple stashes, you can specify which stash to apply.

By following these steps, you should be back on your "stage" branch, and the untracked files will be either removed or stashed, depending on your preference. Please be careful when using git clean as it can result in the permanent deletion of files.


How to recover that commit

git reflog

git checkout -b recovered-branch 05e9e88

git checkout main
git merge recovered-branch



######################################################

```
From https://github.com/devaddmark/behaav
 * branch            behaav     -> FETCH_HEAD
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge (the default strategy)
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

solution:-

To merge and keep local + remote changes:

git pull --no-rebase

Or rebase your local commits on top of remote:

git pull --rebase

If you want to just overwrite local branch with remote:

git fetch origin
git reset --hard origin/behaav