from subprocess import Popen, PIPE


class Process(object):
    @staticmethod
    def run(cmd, ignore_resp=False):
        try:
            process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=-1)
            if ignore_resp:
                status = None
                exec_msg = None
            else:
                output, error = process.communicate()
                returncode = process.returncode
                status = True if returncode == 0 else False
                exec_msg = output if returncode == 0 else error

        except Exception as e:
            status = False
            exec_msg = str(e)

        return status, exec_msg