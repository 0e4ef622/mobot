import subprocess
import re
def help(chat, chatid, username, args):
    chat(chatid, '%s: u kanno haz halpz' % username)

def ping(chat, chatid, username, args):
    chat(chatid, '%s: yes i exist' % username)

def fortune(chat, chatid, username, args):
    chat(chatid, '%s: %s' % (username, str(subprocess.check_output('fortune'),encoding='utf-8')))

def chess(chat, chatid, username, args):
    chat(chatid, '%s: There is no chess yet' % username)

#def Ni(chat, chatid, username):
#    chat(chatid, '%s: No, it\'s Ni!' % username)

def bf(chat, chatid, username, args):
    if len(args) == 0:
        chat(chatid, '%s: This is a BF interpreter. Just stick the BF code after the !bf' % username)
    else:
        code = ''.join(args)
        if re.search(',', code):
            chat(chatid, '%s: You want me to support input?' % username)
            return;

        f = open('/tmp/bf.bf', 'w')
        f.write(code)
        f.close()

        try:
            out = subprocess.check_output(['bf', '/tmp/bf.bf'], stderr=subprocess.STDOUT, timeout=3)
            chat(chatid, '%s: %s' % (username, str(out, encoding='utf-8')))

        except subprocess.TimeoutExpired:
            chat(chatid, '%s: wtf r u trying to do???' % username)
        except subprocess.CalledProcessError as err:
            chat(chatid, '%s: %s' % (username, str(err.output, encoding='utf-8')))

cmds = {
        '!help': help,
        '!ping': ping,
        '!fortune': fortune,
        '!chess': chess,
#       '!Ni': Ni,
        '!bf': bf
        }
