#!/usr/bin/python3
import subprocess
import argparse
import os
import signal

margin_padding_0 = 25
margin_padding_1 = 10


class Progress:
    def __init__(self):
        self.id = -1
        self.open_file_num = -1
        self.exe = ''

    def __repr__(self):
        return "%s%s%d" % (
            format(self.exe, "<%d" % margin_padding_0), format(self.id, "<%d" % margin_padding_1), self.open_file_num)


pids = {}
pid_exe_map = {}
# if you set the `-k n` param, this script will try to kill the most n processes which open too many files.
kill_top_n = 0
# print the top 10 processes
top_n = 10

ans_list = []


def get_openfile_list():
    global ans_list
    # get the pid and exe map
    p2 = subprocess.Popen("ps -e | awk '{print $1,$4}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in p2.stdout.readlines():
        temp = line.decode('utf-8').strip().split()
        if len(temp) != 2:
            print("There is a line with error:\t\n", temp)
        elif temp[0] != 'PID':
            pid_exe_map[int(temp[0])] = temp[1]

    # print(pid_exe_map)

    p = subprocess.Popen("lsof -n|awk '{print $2}'|sort|uniq -c", shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    for line in p.stdout.readlines():
        # print(line)
        temp = line.decode('utf-8').strip().split()
        if len(temp) != 2:
            print("There is a line with error:\t\n", temp)
        elif temp[1] != 'PID':
            a_pid = Progress()
            a_pid.id = int(temp[1])
            a_pid.open_file_num = int(temp[0])
            a_pid.exe = pid_exe_map.get(a_pid.id, '')
            pids[a_pid.id] = a_pid

        # print(pids)
    ans_list = sorted(pids.items(), key=lambda x: x[1].open_file_num, reverse=True)
    print(format("Process Name ", "<%d" % (margin_padding_0 - 1)),
          format("PID", "<%d" % (margin_padding_1 - 1)), "open_file_num")
    list1_top_n = ans_list[:top_n]
    for x in list1_top_n:
        print(x[1])


def work():
    get_openfile_list()
    if kill_top_n > 0:
        print("\nkilling top %d processes" % kill_top_n)
        for i in range(min(kill_top_n, len(ans_list))):
            kill_pid(ans_list[i][1].id)


def kill_pid(pid):
    try:
        os.kill(pid, signal.SIGKILL)
        print('Kill PID %d success' % pid)

    except OSError:
        print('Error: kill %d', pid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve the error of `open too many files`')
    parser.add_argument('-k', '--kill', metavar='kill the most X processes which open too many files', required=False,
                        dest='kill', action='store')
    args = parser.parse_args()
    if args.kill:
        kill_top_n = int(args.kill)
    work()
