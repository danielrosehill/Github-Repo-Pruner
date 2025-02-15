# Development Prompt

Please develop a simple GUI utility for the Linux desktop. Use PyQt6.

The functionality and purpose of the utility is as follows:

## Base module setting

The user will configure a base path on the local operating system where they store Github repositories.

This base path should persist in memory through a simple memory module that can be stored user's configuration directory (~/.config). If you can think of a more appropriate location on the Linux file system to store this simple memory module, choose that instead.

On the first run, the base module will not have been configured. This should not prevent operation. A simple settings UI should allow the user to change and change the base module. 

## Main UI 

The functionality of the UI is to present one repository at a time and the user can either delete it or keep it. 

There should be two modes of operation: The first is an alphabetical mode of operation went to the repositories represented in alphabetical order (according to the folder file names as they are stored on the local system). The second mode of operation is randomized, in which the repositories are presented at random. 

### Repo display

Each repository should be presented to the user in the following manner:

My Github Repository
/my-repos-my-github-repo

In the above example:

- "My Github Repository" is the prettified repository name constructed from the folder path
- /my-repos-my-github-repo is the path relative to the base path that the user configured

When each repository presents there are two action buttons:

- Delete
- Keep

If the user chooses delete, the repository is deleted from the local filesystem
If the user chooses "keep" the repository is kept (no action is taken)

After either button press, the next repository automatically loads

In the randomized mode of operation, the display continues indefinitely until the user exits the program. 

In the alphabetical mode of operation The review continues until the last repository is reached, at which point a success message can display saying end of repositories reached.

## Confirmation Indicators

- If the user deletes a repository, there should be a success message saying the repository was deleted. This should display for one second and then the next repository should be automatically loaded. 
- If the user chooses to keep the repository No message is necessary. The UI should simply load the next repository immediately after the press is recorded. 

## Total Repo Count Indicator

At the bottom of the GUI should be a dynamically updating total count of the repositories in the user's file system. The calculation can be the number of top level folders within the base path. As the user deletes repositories, this number should reduce. 

## Other Features

- Use your creativity to think of any UI additions or extra features that would be required. The user doesn't need to be reminded that deleting repositories is a destructive action. 
