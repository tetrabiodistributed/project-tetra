How to Run an Application at Launch on a Raspberry Pi
=====================================================

Running an application at launch is fairly simple.  You simply use the `autostart` system to add to the boot procedure (there are other ways, but `autostart` guarantees that the X windowing system is loaded).  To do this, you need to create a file `/home/pi/.config/autostart/TetraVentilatorSplitter.desktop` (or whatever name `*.desktop`), and add this bit of code to it:

```
[Desktop Entry]
Name=TetraVentilatorSplitter
Exec=# Whatever you run to execute the application
```

Then you can save that file and `sudo reboot` and the Pi will launch into the application specified.

This is based on the tutorial [here](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all).