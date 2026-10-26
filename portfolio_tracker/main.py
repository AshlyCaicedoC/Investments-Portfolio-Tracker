from portfolio_tracker.cli import run


def main ():
    run()


# if this module is executed from the command line then run the main function. 
# However, if this function is imported into another module do not run the main function 
if __name__=="__main__":
    main()