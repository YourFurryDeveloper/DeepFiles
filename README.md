# FsRecord
A Python program that allows you to run a deep scan of all the files and folders in your directory and then view them


## How to use
To record your directory, place `main.py` in the directory you want to record, then run it. It will record the data to a file called `fs.json`.
Here is an example scan of the Repl I used to test this in.
```
{
    "/home/runner/workspace": {
        "stats": {
            "file1": "subvolume_total_bytes",
            "file2": "resources.json",
            "file3": "subvolume_usage_bytes",
            "file4": "scratch_usage_bytes",
            "file5": "scratch_total_bytes",
            "file6": "oom_count"
        },
        "file3": "pending_changes.lock",
        "file4": "pending_snapshot.lock"
    }
}
```
To view the files, run `explorer.py` in the same directory as `fs.json`. It will open up a Tkinter TreeView window showing your recorded filesystem.


**NOTE: Do not use this on your / directory (or any SUPER large directory, for that matter), as it will make the JSON file absolutely MASSIVE in size, and may crash when it goes to dump all the info**
