from os import stat, system
from subprocess import check_output, Popen
import sys, time
from glob import glob

from parse import convert

def main(pfn=None):
	for fn in glob('../SolidWorks Drawings/*.SLDPRT') if pfn is None else [pfn]:
		bfn = fn.rsplit('/', 1)[1].split('.')[0].split('-')[0]
		tfn = '../CModels/' + bfn + '.cm'
		print bfn
		try:
			if pfn is None and stat(tfn).st_mtime >= stat(fn).st_mtime:
				print ' - skipping'
				continue
		except:
			pass
		system('osascript runner.osa')
		time.sleep(1)
		pid = check_output('pgrep eDrawings', shell=True).strip()
		system('osascript killopen.osa')
		popen = Popen(['dtrace', '-p', pid, '-s', 'edrawing_dump.d', '-x', 'evaltime=postinit'], stdout=file('dump.txt', 'w'))
		check_output(['open', fn])
		popen.wait()

		system('kill ' + pid)

		convert('dump.txt', tfn)

if __name__=='__main__':
	main(*sys.argv[1:])
