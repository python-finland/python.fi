import subprocess

def main():
    cmd = subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = cmd.stdout.read()
    # check the output and deploy if there is any update
    if output != 'Already up-to-date.\n':
        subprocess.Popen('~/google_appengine/appcfg.py --passin --email=pythonfinland@gmail.com update src < gaepass', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    main()