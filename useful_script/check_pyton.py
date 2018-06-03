def check_python():
    info = sys.version_info
    if info[0] == '2' and not info[1] >=6:
        print('python 2.6+ is required')
        sys.exit(1)
    elif info[0] == '3' and not info[1] >= 3:
        print("pyton 3.3+ is required")
        sys.exit(1)
    elif info[0] not in [2,3]:
        print('python version not supported')
        sys.exit(1)