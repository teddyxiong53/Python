import select

if hasattr(select, 'epoll'):
    print "has epoll"

if hasattr(select, 'kqueue'):
    print "has kqueue"

if hasattr(select, 'select'):
    print "has select"