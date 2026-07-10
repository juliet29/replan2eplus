from cyclopts import App
from loguru import logger
from utils4plans.logs import logset

app = App()


@app.command()
def welcome():
    # logset()
    print("Welcome to replan2eplus")


def main():
    logset(to_stderr=True)
    logger.enable("geomeppyupdated")
    app()


if __name__ == "__main__":
    main()
