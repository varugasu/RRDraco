from distutils import spawn
import subprocess


class rrdtool:
    tool = spawn.find_executable('rrdtool')

    @classmethod
    def info(cls, rrd_file):
        cmd = [cls.tool, 'info', rrd_file]
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()

    @classmethod
    def create(cls, rrd_file, ds, rra, start="N", step=300):
        if not rrd_file.endswith('.rrd'):
            rrd_file += '.rrd'
        cmd = [cls.tool, 'create', rrd_file,
               '--start', start, '--step', str(step)]
        cmd += ds
        cmd += rra
        return not bool(subprocess.check_call(cmd, stderr=subprocess.STDOUT))
