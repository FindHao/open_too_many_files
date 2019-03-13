# open_too_many_files
A script to solve the error open too many files in linux.

# install

```bash
git clone https://github.com/FindHao/open_too_many_files.git
```
or download release package and unzip it.

# add to your /usr/bin/
```bash
cd open_too_many_files
sudo cp whoisthebadboy.py /usr/bin/
sudo chmod +x /usr/bin/whoisthebadboy.py
```

# usage

You can set the param `-k n` or `--kill n` which means the script will kill the top n processes who open too many files.

```bash
whoisthebadboy.py -k 2
```
The console will show like this:
```bash
Process Name             PID       open_file_num
TIM.exe                  26122     29300
chrome                   18168     25375
thunderbird              5268      23562
java                     13700     22400
insync                   5459      17610
mendeleydesktop          7828      15810
gnome-shell              5003      10984
wps                      10962     10912
TeamViewer               5260      5620
tracker-extract          5303      5104

killing top 1 processes
Kill PID 26122 success

```