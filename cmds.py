import subprocess
import re
def help(chat, chatid, username, argstr):
    chat(chatid, '%s: u kanno haz halpz' % username)

def ping(chat, chatid, username, argstr):
    chat(chatid, '%s: yes i exist' % username)

def fortune(chat, chatid, username, argstr):
    chat(chatid, '%s:\n%s' % (username, str(subprocess.check_output('fortune'),encoding='utf-8')))

def chess(chat, chatid, username, argstr):
    chat(chatid, '%s: There is no chess yet' % username)

#def Ni(chat, chatid, username):
#    chat(chatid, '%s: No, it\'s Ni!' % username)

def bf(chat, chatid, username, argstr):
    if not argstr:
        chat(chatid, '%s: This is a BF interpreter. Just stick the BF code after the !bf' % username)
    else:
        code = argstr
        if re.search(',', code):
            chat(chatid, '%s: Motivate me somehow and I will add support for input' % username)
            return;

        f = open('/tmp/tmp.b', 'w')
        f.write(code)
        f.close()

        try:
            out = subprocess.check_output(['bf', '/tmp/tmp.b'], stderr=subprocess.STDOUT, timeout=3)
            out = str(out, encoding='utf-8')
            chat(chatid, '%s: %s' % (username, out.replace('\x00', '<NULL>')))

        except subprocess.TimeoutExpired:
            chat(chatid, '%s: wtf r u trying to do???' % username)
        except subprocess.CalledProcessError as err:
            chat(chatid, '%s: %s' % (username, str(err.output, encoding='utf-8')))

def snowman(chat, chatid, username, argstr):
    if not argstr:
        chat(chatid, '%s: This is a Snowman interpreter. Just stick the Snowman code after the !snowman' % username)
    else:
        code = argstr
        if re.search('vg', code, re.I):
            chat(chatid, '%s: Motivate me somehow and I will add support for input' % username)
            return;

        f = open('/tmp/snowman', 'w')
        f.write(code)
        f.close()

        try:
            out = subprocess.check_output(['./snowman', '/tmp/snowman'], stderr=subprocess.STDOUT, timeout=3)
            out = str(out, encoding='utf-8')
            chat(chatid, '%s: %s' % (username, out.replace('\x00', '<NULL>')))

        except subprocess.TimeoutExpired:
            chat(chatid, '%s: wtf r u trying to do???' % username)
        except subprocess.CalledProcessError as err:
            chat(chatid, '%s: %s' % (username, str(err.output, encoding='utf-8')))

def dorp(chat, chatid, username, argstr):
    chat(chatid, 'I agree')

def wtf(chat, chatid, username, argstr):
    cmd = ["wtf"]
    arg = argstr.split()
    cmd = cmd + arg
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=3)
        out = str(out, encoding='utf-8')
        chat(chatid, '%s: %s' % (username, out.replace('\x00', '<NULL')))
    except subprocess.TimeoutExpired:
        chat(chatid, '%s: DOOD WHAT THE FUCK DID YOU DO‽' % username)
    except subprocess.CalledProcessError as err:
        chat(chatid, '%s: %s' % (username, str(err.output, encoding='utf-8')))

cmds = {
        '!help': help,
        '!ping': ping,
        '!fortune': fortune,
        '!chess': chess,
#       '!Ni': Ni,
        '!bf': bf,
        '!snowman': snowman,
        'dorp': dorp,
        '!wtf': wtf
        }
