class AddingExistingUser(Exception):
    """Exception class when trying to create an existing user."""

    def __str__(self) -> str:
        return "A user with this name already exists."


class AddingExistingPhone(Exception):
    """Exception class when trying to add an existing phone."""

    def __str__(self) -> str:
        return "This user already has this phone number."

class AddingExistingBirthday(Exception):
    """Exception class when trying to add an existing date of birth."""

    def __str__(self) -> str:
        return "This user already has this date of birth."


class InvalidPhoneNumber(Exception):
    """Exception raised for an invalid phone number format."""

    def __str__(self) -> str:
        return "Phone number format is incorrect."


class InvalidBirthday(Exception):
    """Exception raised for an invalid birthday format."""

    def __str__(self) -> str:
        return "Birthday format is incorrect."


class NonExistentUser(Exception):
    """Exception class when attempting to change a non-existent user."""

    def __str__(self) -> str:
        return "User with that name does not exist."


class EmptyUsernameError(Exception):
    """Exception class when no username is specified."""

    def __str__(self) -> str:
        return "Please enter username."


class EmptyPhoneError(Exception):
    """Exception class when no phone is specified."""

    def __str__(self) -> str:
        return "Please enter phone number."


class EmptyBirthdayError(Exception):
    """Exception class when no birthday is specified."""

    def __str__(self) -> str:
        return "Please enter date of birth."



def input_error(funk):
    """Decorator function to handle input errors.

    Args:
        funk (function): The function to be decorated.

    Returns:
        function: The decorated function."""

    def inner(*args, **kwargs):
        """Inner function of the input_error decorator.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the decorated function or an error message.

        Raises:
            EmptyUsernameError: If no username is specified.
            KeyError: If the name of an existing user is not entered.
            UnboundLocalError: If username and phone number are not entered.
            AddingExistingUser: If a user with the same name already exists.
            InvalidPhoneNumber: If the phone number format is incorrect.
            NonExistentUser: If the user does not exist."""

        try:
            return funk(*args, **kwargs)
        except EmptyUsernameError as err:
            return err
        except KeyError:
            return "Please enter the name of an existing user"
        except UnboundLocalError:
            return "Please enter username and phone number"
        except AddingExistingUser as err:
            return err
        except AddingExistingPhone as err:
            return err
        except InvalidPhoneNumber as err:
            return err
        except NonExistentUser as err:
            return err
        except InvalidBirthday as err:
            return err
        except EmptyPhoneError as err:
            return err
        except EmptyBirthdayError as err:
            return err
        except AddingExistingBirthday as err:
            return err

    return inner