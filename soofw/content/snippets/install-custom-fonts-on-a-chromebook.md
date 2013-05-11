* title = Install Custom Fonts on a Chromebook
* datetime = 2/20/2013 12:07am
* tags = chrome

	$ sudo /usr/share/vboot/bin/make_dev_ssd.sh --remove_rootfs_verification
	$ sudo /usr/share/vboot/bin/make_dev_ssd.sh --remove_rootfs_verification --partitions X
	$ sudo reboot
	$ sudo cp /path/to/font.ttf /usr/share/fonts/
	$ sudo reboot

Should work. I hope.
