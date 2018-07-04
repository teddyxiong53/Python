import shell

def main():
    shell.check_python()
    config = shell.get_config(True)
    print (config)
if __name__ == '__main__':
    main()