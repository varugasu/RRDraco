from distutils import spawn
import subprocess

rrdtool_exec = spawn.find_executable('rrdtool')


class rrdtool:

    @staticmethod
    def info(rrd_file):
        cmd = [rrdtool_exec, 'info', rrd_file]
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()

    @staticmethod
    def create(rrd_file, ds, rra, start="N", step=300):
        if not rrd_file.endswith('.rrd'):
            rrd_file += '.rrd'
        cmd = [rrdtool_exec, 'create', rrd_file,
               '--start', start, '--step', str(step)]
        cmd += ds
        cmd += rra
        return not bool(subprocess.check_call(cmd, stderr=subprocess.STDOUT))
