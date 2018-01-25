#!/usr/bin/env python
#
# https://stackoverflow.com/questions/39048654/how-to-enable-directory-indexing-on-github-pages 
#
""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""
from __future__ import print_function
import os.path, time

import subprocess
import sys
def run(cmd):
    cmd = cmd.split(' ')
    try :
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        # print (e.args)
        # sys.exc_info()[1]
        print("ERROR:", sys.exc_info()[1])
        return
    stdout, stderr = output.communicate()
    if len(stdout) != 0:
        for line in stdout.decode("utf-8").split('\n'):
            print(line)
    if len(stderr) != 0:
        for line in stderr.decode("utf-8").split('\n'):
            print(line)



INDEX_TEMPLATE = r"""

<html>
<head>
<title>${header}</title>
<meta name="description" content="${header}"/>

</head>
<body>
    <h2><a href='https://rzbhatti.github.io/p3m'>P3M</a></h2>
    <p>
    <table>
        <tbody>
             % for name in dirnames:
            <tr>
                <td valign="top"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAd5JREFUeNqMU79rFUEQ/vbuodFEEkzAImBpkUabFP4ldpaJhZXYm/RiZWsv/hkWFglBUyTIgyAIIfgIRjHv3r39MePM7N3LcbxAFvZ2b2bn22/mm3XMjF+HL3YW7q28YSIw8mBKoBihhhgCsoORot9d3/ywg3YowMXwNde/PzGnk2vn6PitrT+/PGeNaecg4+qNY3D43vy16A5wDDd4Aqg/ngmrjl/GoN0U5V1QquHQG3q+TPDVhVwyBffcmQGJmSVfyZk7R3SngI4JKfwDJ2+05zIg8gbiereTZRHhJ5KCMOwDFLjhoBTn2g0ghagfKeIYJDPFyibJVBtTREwq60SpYvh5++PpwatHsxSm9QRLSQpEVSd7/TYJUb49TX7gztpjjEffnoVw66+Ytovs14Yp7HaKmUXeX9rKUoMoLNW3srqI5fWn8JejrVkK0QcrkFLOgS39yoKUQe292WJ1guUHG8K2o8K00oO1BTvXoW4yasclUTgZYJY9aFNfAThX5CZRmczAV52oAPoupHhWRIUUAOoyUIlYVaAa/VbLbyiZUiyFbjQFNwiZQSGl4IDy9sO5Wrty0QLKhdZPxmgGcDo8ejn+c/6eiK9poz15Kw7Dr/vN/z6W7q++091/AQYA5mZ8GYJ9K0AAAAAASUVORK5CYII= "
                    alt="[DIR]"></td>
                <td><a href="${name}">${name}</a></td>
                <td>&nbsp;</td>
            </tr>
            % endfor
            % for name in filenames:
            <tr>
                <td valign="top"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAABHUlEQVR42o2RMW7DIBiF3498iHRJD5JKHurL+CRVBp+i2T16tTynF2gO0KSb5ZrBBl4HHDBuK/WXACH4eO9/CAAAbdvijzLGNE1TVZXfZuHg6XCAQESAZXbOKaXO57eiKG6ft9PrKQIkCQqFoIiQFBGlFIB5nvM8t9aOX2Nd18oDzjnPgCDpn/BH4zh2XZdlWVmWiUK4IgCBoFMUz9eP6zRN75cLgEQhcmTQIbl72O0f9865qLAAsURAAgKBJKEtgLXWvyjLuFsThCSstb8rBCaAQhDYWgIZ7myM+TUBjDHrHlZcbMYYk34cN0YSLcgS+wL0fe9TXDMbY33fR2AYBvyQ8L0Gk8MwREBrTfKe4TpTzwhArXWi8HI84h/1DfwI5mhxJamFAAAAAElFTkSuQmCC "
                    alt="[DIR]"></td>
                <td><a href="${name}">${name}</a></td>
                <td>&nbsp;</td>
            </tr>
            % endfor
            </p>
        </tbody>
    </table>
</body>
</html>
"""

EXCLUDED = ['index.html','make_index.py']

import os
import argparse

# May need to do "pip install mako"
from mako.template import Template

def fun(dir,rootdir):
    print('Processing: '+dir)
    filenames = [fname for fname in sorted(os.listdir(dir))
              if fname not in EXCLUDED and os.path.isfile(dir+fname)]
    dirnames = [fname for fname in sorted(os.listdir(dir))
            if fname not in EXCLUDED  ]
    dirnames = [fname for fname in dirnames if fname not in filenames]
#    header = os.path.basename(dir)
    f = open(dir+'/index.html','w')
    print(Template(INDEX_TEMPLATE).render(dirnames=dirnames,filenames=filenames, header='P3M @ Git',ROOTDIR=rootdir,time=time.ctime(os.path.getctime(dir))),file=f)
    f.close()
    for subdir in dirnames:
        try:
            fun(dir+subdir+"/",rootdir+'../')
        except:
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    fun(args.directory+'/','../')
    run('git add .')
    run('git commit -m\"Updated\" .')
    run('git push')

if __name__ == '__main__':
    main()

