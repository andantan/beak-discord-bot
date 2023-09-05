def config_args():
    import argparse

    parser = argparse.ArgumentParser(description='Beak discord utility bot arguments')

    parser.add_argument(
        "-d", "--debug",
        dest="DEBUG",
        action="store_true",
        required=False,
        help="Run beak as debug mode - Only admin can execute commands"
    )

    parser.add_argument(
        "-p", "--patch",
        dest="PATCH",
        action="store_true",
        required=False,
        help="Run beak as patch mode - User can execute commands except play command"
    )

    return parser.parse_args()


def config_envs() -> None: 
    import dotenv
    dotenv.load_dotenv(verbose=True)
