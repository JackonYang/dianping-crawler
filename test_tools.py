# -*- Encoding: utf-8 -*-


def request(url, filename):
    print '\n---------------- requesting ------------'
    print 'url: {}'.format(url)
    print 'filename: {}'.format(filename)
    print ''
    with open('testdata.html', 'r') as f:
        text = ''.join(f.readlines())
    return text


def request_pages(key, page_range, url_ptn, find_items, resend=3,
                  min_num=0, max_failed=5, filename_ptn=None):
    print '\n---------------- requesting pages ------------'
    for i in page_range[:3]:  # first 3 pages
        print 'url: {}'.format(url_ptn.format(key=key, page=i))
        print 'filename: {}'.format(filename_ptn.format(key, i))
    print ''

    with open('testdata.html', 'r') as f:
        text = ''.join(f.readlines())
    return find_items(text, key)
