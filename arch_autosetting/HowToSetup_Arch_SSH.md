# ArchLinuxインストールガイド(SSH ver.)
## はじめに
SSHを利用してVirtualBox上のArchをセッティングする。

## 目次
1. SSHのためのVirtualBoxの設定
2. ArchLinux on VirtualBox
3. ホストのSSHログイン
4. パティーショニング/マウンティング/マウント
5. インストール
6. chrootでの作業
7. GRUBのインストール

### 1.SSHのためのVirtualBoxの設定
- 設定-システムでEFIを有効化
- 設定-ネットワーク-高度-ポートフォワーディング-ポート追加
ホストポートを4093,ゲストポートを59623に

### 2.ArchLinux on VirtualBox
アンダースコア一箇所打つ
~~~code
loadkeys jp106 // type
passwd // type
0138 // type
0138 // type
systemctl start sshd // type
vi /etc/ssh/sshd // type --no_enter
3 // wait
config // type
2 // wait
13Gxlllllxxi 59623 // type
esc // press
ZZ // type
systemctl restart sshd // type
~~~

### 3.ホストのsshログイン
ここからホストに移動
~~~code
ssh-keygen -R '[localhost]:4093'
ssh -p 4093 root@localhost
1 // wait
yes
0138
~~~

### 4.パティーショニング/マウンティング/マウント
~~~code
timedatectl set-ntp true 
parted /dev/sda
mklabel gpt
mkpart ESP fat32 1MiB 551MiB
set 1 esp on
mkpart primary ext4 551MiB 100%
print
quit
mkfs.vfat -F32 /dev/sda1
mkfs.ext4 /dev/sda2
1 // wait
mount /dev/sda2 /mnt
mkdir -p /mnt/boot
mount /dev/sda1 /mnt/boot
~~~

### 5.インストール
~~~code
vi /etc/pacman.d/mirrorlist
6Gi // type
Server = http: // clip --no_enter
2 // wait
ftp.tsukuba.wide.ad.jp/Linux/archlinux/$repo/os/$arch
esc // press
ZZ // type --no_enter
pacstrap /mnt base base-devel linux-lts vim
~~~
 
### 6.chrootでの作業
echo localhost > /etc/hostname
vim /etc/hosts
jo //type
baskspace // press --no_enter
baskspace // press --no_enter
baskspace // press --no_enter
baskspace // press --no_enter
127.0.0.1       localhost
::1             localhost
127.0.1.1       localhost.localdomain localhost
esc // press --no_enter
ZZ //type
pacman -S dhcpcd
Y
1 // wait
systemctl enable dhcpcd
passwd
0138
0138

~~~code
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt /bin/bash
vim /etc/locale.gen
176Gx301GxZZ  // type
locale-gen
2.5 // wait
echo LANG_en=US.UTF-8 > /etc/locale.conf
export LANG_en=US.UTF-8
ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
hwclock --systohc --utc
0.5 // wait
vim /etc/vconsole.conf
i // type --no_enter
KEYMAP_jp106
FONT_lat9w-16
esc // press --no_enter
ZZ // type
echo localhost > /etc/hostname
vim /etc/hosts
jo // type
backspace // press --no_enter
backspace // press --no_enter
backspace // press --no_enter
backspace // press --no_enter
127.0.0.1       localhost
::1             localhost
127.0.1.1       localhost.localdomain localhost
esc // press --no_enter
ZZ // type
pacman -S dhcpcd
Y
2 // wait
systemctl enable dhcpcd
passwd
0138
0138
~~~

### 7.GRUBのインストール
~~~code
pacman -S grub dosfstools efibootmgr
Y
2 // wait
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=arch_grub --recheck
grub-mkconfig -o /boot/grub/grub.cfg
3 // wait
mkdir /boot/EFI/boot
cp /boot/EFI/arch_grub/grubx64.efi  /boot/EFI/boot/bootx64.efi
exit
umount -R /mnt
shutdown -h now
~~~

### 8.
-設定-ストレージ-ストレージデバイス-arch.isoを選択-右のCDアイコン-ディスクを除去
