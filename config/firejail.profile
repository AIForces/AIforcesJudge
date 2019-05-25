blacklist /bin
blacklist /home
blacklist /lib32
blacklist /sys
blacklist /vmlinuz
blacklist /boot
blacklist /initrd.img
blacklist /vmlinuz.old
blacklist /dev
blacklist /initrd.img.old
blacklist /libx32
blacklist /opt
blacklist /sbin
blacklist /lost+found
blacklist /srv
blacklist /var
read-only /
disable-mnt
private-etc judge
private-tmpapparmor
caps.drop all
seccomp
memory-deny-write-execute
nonewprivs
noroot
x11 none
nodvd
nogroups
shell none
nodbus
nosound
noautopulse
notv
nou2f
novideo
no3d
net none
rlimit-as 123456789012
rlimit-cpu 123
rlimit-nproc 0
rlimit-sigpending 0
