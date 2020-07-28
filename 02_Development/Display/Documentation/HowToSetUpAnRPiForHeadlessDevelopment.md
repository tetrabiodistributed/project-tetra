How to set up a Raspberry Pi for headless developement
======================================================

Writing software for a Raspberry Pi is an interesting challenge because the outcome of the software often depends on the particular hardware configuration of the Pi, especially if you're writing software that uses sensors and other auxilliarly hardware.  The easiest way to write software then is to connect a monitor and keyboard to the Pi and do development directly on the hardware.  However, this is suboptimal because you can't necessarily use your favorite text editor, and Pis up through the 3B+ can only connect to one monitor.  A better solution is to do headless development where you send files from your big computer to the Pi over a network communication protocol.

To make this happen, you're going to need to set up SSH on the Pi and SFTP communication on you big computer.

SSH
---

There are many online tutorials to set up SSH on the Pi.  I think [this one]() is good.  Also as a quality-of-life thing, you can add your Pi's IP address to `/etc/hosts` so you don't have to type out the whole IP every time.

After you've done all that, you'll need to get onto your Pi with a monitor and keyboard and enter `ssh [username]@[hostname]` into the the terminal.  Then you can remove your monitor and keyboard from the Pi for good.  Enter `ssh [username]@[hostname]` into your big computer's terminal and you'll be set.

SFTP
----

The details of how to set up SFTP will depend on your text editor.  I'll show how to do this for Sublime Text.

1. First, make sure the package manager is set up.  Open the command palette with Ctrl+Shift+P (Linux/Windows) or Cmd+Shift+P (Mac) and type `Install Package Control` and hit Enter
2. Again open the command palette and type `Package Control: Install Package` and hit Enter
3. In the text box that pops up after you hit Enter, type `SFTP` and select the first option that comes up (the description should say something like "Commercial SFTP/FTP plugin - upload, sync, browse, remote edit, diff and vcs integration")
4. Open the root directory for your project with Sublime such that you see the side bar with all the files in it.  Right click on the root folder and from the Tooltip menu select `SFTP>Map to Remote...`
5. This will create a file `sftp-config.json` in your project's root directory that defines how the SFTP plugin will connect to your Pi.  Make sure to add this file to your `.gitignore` because it'll contain sensitive information like a password.
6. Enter your Pi's IP address for the `"host"` field, your username on the Pi (by default `pi`) for the `"username"` field, and your password for the Pi for the `"password"` field (make sure you have a password on your Pi if you don't already).
7. By default, you need to manually tell the SFTP program which file to upload to the Pi when.  But if you set `"upload_on_save"` to `true`, then it'll upload every time you save.

Once you've got SSH and SFTP set up, you can just write code, it'll update on the Pi automatically, and the you can test you code in the Pi's terminal on your big computer.
