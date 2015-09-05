import subprocess
import re
def help(chat, chatid, dispname, argstr):
    chat(chatid, '%s: u kanno haz halpz' % dispname)

def halp(chat, chatid, dispname, argstr):
    chat(chatid, '%s: %s' % (dispname, ", ".join(cmds.keys())))

def ping(chat, chatid, dispname, argstr):
    chat(chatid, '%s: yes i exist' % dispname)

def fortune(chat, chatid, dispname, argstr):
    chat(chatid, '%s:\n%s' % (dispname, str(subprocess.check_output('fortune'),encoding='utf-8')))

def chess(chat, chatid, dispname, argstr):
    chat(chatid, '%s: Motivate me and I just may add chess' % dispname)

#def Ni(chat, chatid, dispname):
#    chat(chatid, '%s: No, it\'s Ni!' % dispname)

def bf(chat, chatid, dispname, argstr):
    if not argstr:
        chat(chatid, """%s: This is a BF interpreter. Here be example:

!bf ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.

Here be example with input

!bf -,+[-[>>++++[>++++++++<-]<+<-[>+>+>-[>>>]<[[>+<-]>>+>]<<<<<-]]>>
>[-]+>--[-[<->+++[-]]]<[++++++++++++<[>-[>+>>]>[+[<+>-]>+>>]<<<<<-]>
>[<+>-]>[-[-<<[-]>>]<<[<<->>-]>>]<<[<<+>>-]]<[-]<.[-]<-,+]
__INPUT__
stuff to rot13""" % dispname)
    else:
        stuff = argstr.split("\n__INPUT__\n")
        code = stuff[0]
        if len(stuff) > 1:
            stdin = "\n__INPUT__\n".join(stuff[1:])
        else:
            stdin = ""

        f = open('/tmp/tmp.b', 'w')
        f.write(code)
        f.close()

        try:
            process = subprocess.Popen(['bf', '/tmp/tmp.b'], stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write(bytes(stdin, encoding="utf-8"))
            process.stdin.close()
            process.wait(timeout=3)
            out = str(process.stdout.read(), encoding='utf-8')
            chat(chatid, '%s: %s' % (dispname, out.replace('\x00', '<NULL>')))

        except subprocess.TimeoutExpired:
            chat(chatid, '%s: wtf r u trying to do???' % dispname)
            process.kill()
        except subprocess.CalledProcessError as err:
            chat(chatid, '%s: %s' % (dispname, str(err.output, encoding='utf-8')))

def snowman(chat, chatid, dispname, argstr):
    if not argstr:
        chat(chatid, """%s: This is a Snowman interpreter. Here be example:

!snowman ("Hello, World!"sp

Here be example with input

!snowman (vgsp
__INPUT__
this be input""" % dispname)
    else:
        stuff = argstr.split("\n__INPUT__\n")
        code = stuff[0]
        if len(stuff) > 1:
            stdin = "\n__INPUT__\n".join(stuff[1:])
        else:
            stdin = ""

        f = open('/tmp/snowman', 'w')
        f.write(code)
        f.close()

        try:
            process = subprocess.Popen(['./snowman', '/tmp/snowman'], stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write(bytes(stdin, encoding="utf-8"))
            process.stdin.close()
            retcode = process.wait(timeout=3)
            if retcode == -11:
                chat(chatid, '%s: Segmentation fault' % dispname)
            else:
                out = str(process.stdout.read(), encoding='utf-8')
                chat(chatid, '%s: %s' % (dispname, out.replace('\x00', '<NULL>')))

        except subprocess.TimeoutExpired as err:
            chat(chatid, '%s: Timeout expired.' % dispname)
            process.kill()

def dorp(chat, chatid, dispname, argstr):
    chat(chatid, 'I agree')

def wtf(chat, chatid, dispname, argstr):
    cmd = ["wtf"]
    arg = argstr.split()
    cmd = cmd + arg
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=3)
        out = str(out, encoding='utf-8')
        chat(chatid, '%s: %s' % (dispname, out.replace('\x00', '<NULL')))
    except subprocess.TimeoutExpired:
        chat(chatid, '%s: DOOD WHAT THE FUCK DID YOU DO‽' % dispname)
    except subprocess.CalledProcessError as err:
        chat(chatid, '%s: %s' % (dispname, str(err.output, encoding='utf-8')))

cmds = {
        '!help': help,
        '!halp': halp,
        '!halpz': halp,
        '!halps': halp,
        '!ping': ping,
        '!fortune': fortune,
        '!chess': chess,
#       '!Ni': Ni,
        '!bf': bf,
        '!snowman': snowman,
        'dorp': dorp,
        'd0rp': dorp,
        '!wtf': wtf
        }
