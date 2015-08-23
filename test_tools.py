# -*- Encoding: utf-8 -*-


def request(url, filename):
    print '\n---------------- requesting ------------'
    print 'url: {}'.format(url)
    print 'filename: {}'.format(filename)
    print ''
    with open('testdata.html', 'r') as f:
        text = ''.join(f.readlines())
    return text
