import urllib.parse
from prettytable import PrettyTable

req = 'http://www.pierobon.org:80/long/path/to/review1.html?submit=yes&action=go#second'

p = urllib.parse.urlparse(req)
s = urllib.parse.urlsplit(req)

t = PrettyTable()
t.field_names = ['Field', 'urlparse', 'urlsplit']
t.add_row(['scheme', p.scheme, s.scheme])
t.add_row(['netloc', p.netloc, s.netloc])
t.add_row(['path', p.path, s.path])
t.add_row(['params', p.params, ''])
t.add_row(['query', p.query, s.query])
t.add_row(['fragment', p.fragment, s.fragment])
t.add_row(['username', p.username, s.username])
t.add_row(['password', p.password, s.password])
t.add_row(['hostname', p.hostname, s.hostname])
t.add_row(['port', p.port, s.port])

print(t)
print(urllib.parse.parse_qs(p.query))
