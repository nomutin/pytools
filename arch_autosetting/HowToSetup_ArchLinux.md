# ArchLinuxインストールガイド
##はじめに
このガイドでは、ArchLinuxをVirtualBox上で
GUI環境構築まで行うためのコマンドを記録する。
なおコードはpythonファイルで自動入力させるために
必ずチルダ三つで囲む。コード上[]で囲まれたものは
プログラム用の特殊操作を表す。

##目次
1. 入力設定
2. パティーショニング
3. フォーマッティング
4. マウンティング
5. ミラーの選択
6. インストール
7. Fstabの作成
8. システム設定
9. ホスト名の設定

##CUI操作
###1.入力設定
~~~code
loadkeys jp106  # 日本語キーボードレイアウトに変更
setfont lat9w-16  # 文字化け防止のためフォントを変更
~~~
なお、下記のコマンドで使用可能なキーマップが調べられる
```
localectl list-keymaps
```

###2.パティーショニング
PCがBIOSモードで起動するならMBRを用いる。MBRのコマンドはfdiskかcfdisk
(UEFIはgdisk)。それぞれのパティーションはフォーマットされることで使えるようになる。

~~~code
fdisk /dev/sda
o
n
[enter]
[enter]
[enter]
:250M
N
n
[enter]
[enter]
[enter]
[enter]
N
w
~~~
上記の設定では、BIOSのfdiskで、250MBの起動用パティーション
(boot用・本当に必要かは分からない)とその残りをシステム・データすべてにしている。

なおパティーショニングは
```
fdisk -l　/dev/sda
```
で確認することができる。

###3.フォーマッティング
~~~code
mkfs.vfat -F32 /dev/sda1
mkfs.ext4 /dev/sda2 
[wait 1]
y
~~~

###4.マウンティング
インストールの前に、パティーションをマウントする必要がある
~~~code
mkdir -p /mnt/boot
mount /dev/sda1 /mnt/boot
mount /dev/sda2 /mnt
timedatectl set-ntp true  # このタイミングでシステムクロックの更新を行う
~~~

###5.ミラーの選択
archのインストールの高速化のため
~~~code
vi /etc/pacman.d/mirrorlist
?Japan
jdd1GjjjjjpZZ
~~~

###6.インストール
ここではbaseとbase_develをインストール
参考：https://qiita.com/suzukeno/items/a978b2de8a34b9a91c95
~~~code
pacstrap /mnt base base-devel vim 
[wait 360]
~~~

###7.Fstabの作成
起動時に自動的にマウントするパーティションなどのファイルシステムを定義する

Fstabファイルを作成しておかないと、HDDへの書き込み権限がなくなる、
エラーが起きてもgenfstabは再度行わない。修正する場合は エディタで/mnt/etc/fstabを修正する。
~~~code
genfstab -U /mnt >> /mnt/etc/fstab
~~~

###8.システム設定
ルートを切り替えてインストールしたArchLinux内で作業を行う
~~~code
arch-chroot /mnt /bin/bash
vim /etc/locale.gen  
176Gx301GxZZ  # UTF-8のコメントアウトを解除
locale-gen  # localeの設定
[wait 2]
~~~

環境変数LANGの編集、アンダースコア・イコールが打てないので苦肉の策↓
~~~code
  # echo LANG=en_US.UTF-8 > /etc/locale.conf  _が打てない
  # export LANG=en_US.UTF-8
[echo LANG]
[wait 5]
US.UTF-8 > /etc/locale.conf
[export LANG]
[wait 5]
US.UTF-8
ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime  # タイムゾーン設定
hwclock --systohc --utc  # ハードウェアクロックの設定
~~~
注：この時点でwifi関係のこと、キーボードレイアウトの固定は行っていない

###9.ホスト名・パスワードの設定
~~~tcode
echo arch > /etc/hostname
passwd
0138
0138
~~~

###10.GRUBのインストール
OSを起動するためのブートローダGRUBをインストールする必要がある
~~~tcode
pacman -S grub os-probe
Y
[wait 5]
  # grub-install --target=i386-pc /dev/sda
[grub-install --target]
[wait 4]
i386-pc /dev/sda
[wait 1]
grub-mkconfig -o /boot/grub/grub.cfg
[wait 1]
~~~








