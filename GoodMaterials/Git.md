# Only clone the sub-folder of a repo from GitHub

Check the original post here, [Cloning specific folders from git](http://scriptedonachip.com/git-sparse-checkout). Basically, it clones everything down, but prunes afterwards.

1. make a directory we want to copy folders to

`$ mkdir example-dir`

`$ cd example-dir`

2. initialize the empty local repo

`$ git init`

3. add the remote origin

`$ git remote add origin -f https://SOME-REPO.git`

4. Tell git we are checking out specifics

`$ git config core.sparsecheckout true`

5. recursively checkout examples folder

`$ echo "example-dir/*" >> .git/info/sparse-checkout`

6. go only 2 depths down the examples directory

`$ git pull --depth=2 origin master`
