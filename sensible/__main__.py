import argparse  # pragma: no cover
import enum

from . import BaseClass, base_echo_server, base_echo_client

# https://stackoverflow.com/a/60750535
class EnumAction(argparse.Action):
    """
    Argparse action for handling Enums
    """
    def __init__(self, **kwargs):
        # Pop off the type value
        enum_type = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum_type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        kwargs.setdefault("choices", tuple(e.value for e in enum_type))

        super(EnumAction, self).__init__(**kwargs)

        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        value = self._enum(values)
        setattr(namespace, self.dest, value)

class ServerType(enum.Enum):
    Client = "client"
    Server = "server"

def main() -> None: # pragma: no cover
    """
    The main function executes on commands:
    `python -m sensible` and `$ sensible `.

    This is your program's entry point.
    """
    parser = argparse.ArgumentParser(
        description="sensible.",
        epilog="Enjoy the sensible functionality!",
    )
    parser.add_argument('type',
                        type=ServerType,
                        action=EnumAction)
    
    # This is required positional argument
    # parser.add_argument(
    #     "name",
    #     type=str,
    #     help="The username",
    #     default="ErnestKz",
    # )

    # This is optional named argument
    # parser.add_argument(
    #     "-m",
    #     "--message",
    #     type=str,
    #     help="The Message",
    #     default="Hello",
    #     required=False,
    # )
    # parser.add_argument(
    #     "-v",
    #     "--verbose",
    #     action="store_true",
    #     help="Optionally adds verbosity",
    # )
    
    args = parser.parse_args()
    # print(f"{args.message} {args.name}!")
    # if args.verbose:
    #     print("Verbose mode is on.")

    print("Executing main function")
    if args.type == ServerType.Client:
        base_echo_client()
    elif args.type == ServerType.Server:
        base_echo_server()
    else:
        raise Exception(args.type + " is not handled.")
    print("End of main function")


if __name__ == "__main__":  # pragma: no cover
    main()
