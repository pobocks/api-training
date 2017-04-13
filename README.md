# MARAC_API_Workshop
These are the resources used in the "There's An API for that!" workshops sponsored by the Mid-Atlantic Regional Archives Conference in 2017. Note that these are the scripts used in the workshop itself. For additional scripts and resources referenced in the workshop, navigate to the _additional resources_ subfolder, above.

These scripts and this documentation, combined with the workshop itself, are meant to encourage and empower users to run Python scripts at their home institutions. The following details are meant to be understood in order.


### How do I use these?

First, a necessary disclaimer: **We highly recommend AGAINST making any changes or using any of these scripts against your working, or Production, instance of ArchivesSpace.** If you do not have a Development version of AS, see the take home documentation for advice on how to ask for one. Note that GET scripts are not that risky, so if you cannot or will not have a Dev instance of AS, you can still try GETs as your familiarize yourself with our scripts. If fear of making mistakes is holding you back, and rightly so, you should investigate options for running a Dev or Virtual Machine (VM) of AS. If your insutition decides to ramp up its use of APIs, a testing environment is a necessity.

Second, remember the vagrant box that you were provided in the course of the workshop. That vagrant, now stored locally on the laptop you brought to the workshop, is our gift to you. We encourage truly novice users who may be wary to try anything on real data to play in the vagrant environment first. No matter what you do there you cannot break anything, and if you mess up your data, just `vagrant destroy` and `vagrant up` again!

There's very little data in the default box, but once you have it up and running you can:
+ manually enter data just like you would in AS
+ import your own collections via EAD
+ more advanced users can use our GET scripts to pull down resource records from your own AS and POST them to the vagrant (remember that the vagrat endpoint will begin with http://localhost:8089)


### How do I _run_ these?
This is a subtly different question from the above. This section gives practical advice for how to run these scripts, though it still raises more questions than answers. The first thing you need to know is what operating system (OS) you are using, and what OS architecture underlies the system you want to communicate to. So for example, ArchivesSpace is Linux-based, and Windows cannot communicate directly with a Linux-based app, but OS X (Macs) can.

* *All users*

   Directories really matter. Whatever directory you download a script to is where a) you need to run that script _from_, b) where that script is going to look for other scripts or files if it's a script that needs other resources (like the barcodes script), and c) put the output files, if the script is creating outputs. So if you download a script and leave it in your Downloads folder, all your resulting output files will also write to that folder. Also, you'll need to navigate to where your scripts are from within the command line/terminal, which is a barrier to novice users. Google "how to change directories in [the command line (Windows)] or [terminal (Mac users)] for advice on how to navigate to your script directory.

* *Windows users*

   Windows users who attended the workshop will recall that we took steps to install _cygwin_, which is a "Linux-like environment for Windows making it possible to port software running on POSIX systems (such as Linux, BSD, and Unix systems) to Windows." Cygwin allows Windows to communicate with Linux-like applications. Please see our presentation slides to walk yourself through installing cygwin and the packages required to run our scripts. Keep the cygwin installer around, it comes in handy (see immediately below).

   Pro-tip: If you ever run a script and cygwin says something along the lines of "pip: command not found" it means you're missing a package (in that example, the missing package is called pip). Try Googling the error message and you will almost certainly find other people with the same problem; use their answers to determine what package you need to install, and then re-run the cgywin installer. When you get to the Install Packages screen, there is where to look for packages. This isn't a easy pro-tip, just an insight on how these programs work.

* *Mac users*

   There is a reason why developers love Macs! You should be able to run these scripts directly from the terminal with no problem. However, you may encounter other scripts that don't run: you're probably missing packages. Our best advice is to Google the exact error message that pops up (if one does), and chances are you'll find the solution online.

More FYIs to read  

   1. You'll always need at least two things to run one of our scripts: _the script itself_ and _the secrets.py file_, and they must both be in the same directory.
   2. A brief description of what each script does follows this long introduction. You used each of these scripts in the workshop itself, and so these descriptions will be familiar. These scripts, as opposed to the ones offered in the _additional resources_ subfolder, above, are highly specific to the workshop, but if you're interested in learning Python, it may help to look at a script you've already used.


## Authenticating with [secrets.py](../blob/master/secrets.py)
Note: You're only downloading secrets.py; secrets._pyc_ is created automatically and you do not need to download it.

Several of these scripts used for interacting with the ArchivesSpace API call a separate secrets.py that should be in the following format:

```
backendurl='YOURBACKENDURL'
user='YOURUSER'
password='YOURPASSWORD'
```
Or, more explicitly:
```
backendurl='archivesspace.fakelibrary.edu:8089'
user='archivist21'
password='guest1234'
```
For the vagrant:
```
backendurl='localhost:8089'
user='admin'
password='admin'
```
Once you download, populate this secrets file with your own information.

## postContainerProfiles.py
This script sources from _containerProfiles.json_ to post container profiles into ArchivesSpace. Both files must be downloaded to the same directory for this script to run. You can edit _containerProfiles.json_ if you'd like to try posting in different profiles.

You can run this script by typing `python postContainerProfiles.py` in cygwin/the Mac terminal. Remember that you need to be running cygwin/the Mac ternimal from the directory where the script is stored.

## postBarcodes.py
This script sources from _barcodes.csv_ to post barcodes into ArchivesSpace. Both files must be downloaded to the same directory for this script to run. You can edit _barcodes.csv_ if you'd like to try posting in different barcodes.

## asLinkProfiles.py
This script assigns a single container profile to all the containers in a collection. This can be done in the actual AS interface, but serves as a good example of a more complex script. The first few actions of the script would be a good starting point for any API action that requires identifying all the containers associated with a single collection.

This script first prompts the user for a resource number, goes and fetches all the containers associated with that resource, then prompts the user for a container profile number, and then creates the link between each container and that profile. Note that there must already be container profiles in AS for this script to work.
