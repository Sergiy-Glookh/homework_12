import sys
import os
from address_book import *
import pickle
import re
from exceptions import *


USERS_FILE = 'users.bin'
ab = AddressBook()


def start(file_name: str = USERS_FILE) -> str:
    """
    Starts the address book application.
    Opens the address book file and loads the users into memory.

    Args:
        file_name (str): The name of the file to load the address book from. Defaults to 'users.bin'.

    Returns:
        str: The manual message.

    """

    file_path =  os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        global ab
        ab = load_users(file_path)

    return manual()


def show_all(*_) -> str:
    """Displays all users in the address book.

    Returns:
        str: The string representation of all users in the address book.
    """

    return '\n'.join([user for user in ab])


def load_users(path: str = USERS_FILE) -> AddressBook:
    """Loads the address book from a file.

    Args:
        path (str): The path to the file. Defaults to 'users.bin'.

    Returns:
        AddressBook: The loaded address book.
    """

    with open(path, 'rb') as file:

        return pickle.load(file)


def save_users(path: str = USERS_FILE) -> None:
    """Saves the address book to a file.

    Args:
        path (str): The path to the file. Defaults to 'users.bin'.

    """

    with open(path, 'wb') as file:
        pickle.dump(ab, file)


def separates_name(args: list[str]) -> tuple[str, list[str]]:
    """Separates the name and phone number or birthday from the given arguments.

    Args:
        args (list): List of string arguments.

    Returns:
        tuple: A tuple containing the name (str) and list of string phones and dates (list[str])."""

    index = len(args)
    for i, arg in enumerate(args):
        if re.search(r'\d', arg):
            index = i
            break

    name = ' '.join(args[:index])
    not_name = args[index:]

    return name, not_name


@input_error
def add_new_user(args: list[str]) -> str:
    """Adds a new user to the address book.

    Args:
        args (List[str]): List of string arguments.

    Returns:
        str: The report message.

    """

    name, not_name = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name in ab:
        raise AddingExistingUser


    ab.add_record(Record(Name(name)))
    report = f"{color(name, 'c')} - User added successfully.\n"

    for obj in not_name:

        result = add_phone([name, obj])
        if result == f"{color(obj, 'c')} - Phone number added successfully.\n":
            report += result
            continue
        if result == f"{color(obj, 'r')} - This user already has this phone number.\n":
            report += result
            continue

        result = add_birthday([name, obj])
        if result == f"{color(obj, 'c')} - Birthday added successfully.":
            report += result
            continue

        result = "Format is incorrect."
        report += f"{color(obj, 'r')} - {result}\n"

    return report

@input_error
def remove_user(args: list[str]) -> str:
    """Removes a user from the address book.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The report message.

    """

    name, _ = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    del ab[name]

    return "User deleted successfully"


@input_error
def add_phone(args: list[str]) -> str:
    """Adds a phone number to an existing user.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The report message.
    """

    name, phones  = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    if not phones:
        raise EmptyPhoneError

    report = ''

    for phone in phones:
        result = ab[name].add_phone(Phone(phone))
        status = 'c' if result == "Phone number added successfully." else 'r'
        report += f"{color(phone, status)} - {result}\n"

    return report

@input_error
def change_phone(args: list[str]) -> str:
    """Changes a phone number of a user.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The report message.
    """

    name, phones = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    if len(phones) == 2:
        old_phone, new_phone = phones
    else:
        return "Please enter old and new phone numbers without spaces"

    report = ab[name].edit_phone(Phone(old_phone), Phone(new_phone))

    return report

@input_error
def show_phone(args: list[str]) -> str:
    """Displays all phone numbers of a user.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The string representation of phone numbers.
    """

    name, _ = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    if not ab[name].phones:
        return f"There are no phone number records for the user {name}"

    result = ''
    for phone in ab[name].phones:
        result += phone.value + '\n'

    return result


@input_error
def remove_phone(args: list[str]) -> str:
    """Removes a phone number from an existing user.

    Args:
        args (List[str]): List of string arguments.

    Returns:
        str: The report message.
    """

    name, phones = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    if not phones:
        raise EmptyPhoneError

    report = ''
    for phone in phones:

        result = ab[name].remove_phone(Phone(phone))
        sratus = 'c' if result == "Phone number deleted successfully." else 'r'
        report += f"{color(phone, sratus)} - {result}\n"

    return report



def add_birthday(args: list[str]) -> str:
    """Adds a birthday to an existing user.

    Args:
        args (List[str]): List of string arguments.

    Returns:
        str: The report message.
    """

    name, birthday  = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    if not birthday:
        raise EmptyBirthdayError

    try:
        y, m, d = map(int, re.split(r'[.,-/_]', birthday[0]))
        ab[name].birthday = Birthday(datetime(y, m, d))
    except InvalidBirthday:
        return f"{color(birthday[0], 'r')} - Birthday format is incorrect."

    return  f"{color(birthday[0], 'c')} - Birthday added successfully."


def show_birthday(args: list[str]) -> str:
    """Displays the birthday of a user.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The birthday of the user in the format 'DD.MM.YYYYр'.
    """

    name, _ = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    if not ab[name].birthday:
        return f"There are no birthday record for the user {name}"

    return ab[name].birthday.value.strftime("%d.%m.%Yp")


def birthday_countdown(args: list[str]) -> str:
    """Displays the number of days until the next birthday of a user.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The number of days until the next birthday.

    """

    name, _  = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    days = ab[name].days_to_birthday() if ab[name].birthday else 'Is not known'
    return f"{days} days remain until the birthday of the user {name}"


@input_error
def remove_birthday(args: list[str]) -> str:
    """Removes the birthday of a user.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The report message.
    """

    name, _  = separates_name(args)

    if not name:
        raise EmptyUsernameError

    if name not in ab:
        raise NonExistentUser

    if not ab[name].birthday:
        return f"There are no birthday record for the user {name}"

    ab[name].birthday = None

    return "Birthday deleted successfully."



def find(args: list[str]) -> str:
    """Searches for users by part of their name or phone number.

    Args:
        args (list[str]): List of string arguments.

    Returns:
        str: The search result.
    """

    found_users = ab.search(' '.join(args))
    result = ''
    if found_users:
        for page in found_users:
            result += page
        return result
    return "Nothing was found for your request"


def hello(*_) -> str:
    """Displays a welcome message.

    Returns:
        str: The welcome message.
    """

    return "How can I help you?"


def color(text: str, status: str = 'c') -> str:
    """Adds color to the text based on the status.

    Args:
        text (str): The text to color.
        status (str): The status of the text. Defaults to 'c'.
            h - heading;
            r - required;
            o - optional;
            c - command.

    Returns:
        str: The colored text.
    """

    match status:
        case 'h':
            text = '\033[1m' + text + '\033[0m'
        case 'r':
            text = '\033[31m' + text + '\033[0m'
        case 'o':
            text = '\033[3m\033[34m' + text + '\033[0m'
        case 'c':
            text = '\033[32m' + text + '\033[0m'

    return text


def manual(*_) -> str:
    """Displays the manual for the address book application.

    Returns:
        str: The manual message.
    """

    message = f'''
{color('Address Book', 'h')}
It is a simple address book application that allows users to manage their contacts,
including adding users, adding phone numbers, adding birthdays, and searching for contacts.
The program uses a command-line interface for interaction.

{color('Commands', 'h')}
{color("add user", 'c')} {color('<name>', 'r')} {color('[phone1] [phone2] [birthday]', 'o')} ...: Add a new user to the address book.
{color("remove user", 'c')} {color('<name>', 'r')}: Deleting a user from the address book.

{color('add phone', 'c')} {color('<name> <phone1>', 'r')} {color('[phone2]', 'o')} ...: Add a phone number to an existing user.
{color('change phone', 'c')} {color('<name> <old_phone> <new_phone>', 'r')}: Change a phone number of a user.
{color('show phone', 'c')} {color('<name>', 'r')}: Show all phone numbers of a user.
{color('remove phone', 'c')} {color('<name> <phone1>', 'r')} {color('[phone2]', 'o')} ...: Deleting the phone number from an existing user.

{color('add birthday', 'c')} {color('<name> <date>', 'r')}: Add a birthday to an existing user.
{color('change birthday', 'c')} {color('<name> <date>', 'r')}: Change the birthday of a user.
{color('show birthday', 'c')} {color('<name>', 'r')}: Show the birthday of a user.
{color('when birthday', 'c')} {color('<name>', 'r')}: Show the number of days until the next birthday of a user.
{color('remove birthday', 'c')} {color('<name>', 'r')}: Deleting date of birth from an existing user.

{color('find', 'c')} {color('<query>', 'r')}: Search for users by part of their name or phone number.
{color('show all', 'c')}: Show all users in the address book.
{color('hello', 'c')}: Display a welcome message.
{color('help', 'c')}: Show the list of available commands.
To exit the program, you can use one of the following commands: \
{color('exit', 'c')}, {color('close', 'c')}, {color('goodbye', 'c')}, {color('quit', 'c')}, or {color('q', 'c')}.

Note:
• Parameters enclosed in {color('<angle brackets>', 'r')} and {color('[square brackets]', 'o')} \
are placeholders that should be replaced with the actual values.
• Parameters enclosed in {color('<angle brackets>', 'r')} are required and must be provided.
• Parameters enclosed in {color('[square brackets]', 'o')} are optional and can be omitted.
• Name must not contain numbers.
• Phone numbers and birthdates should be entered without spaces in between the digits, allowing separators: {color('.,-/_', 'o')}.
• The date should be in the format YYYY-MM-DD.
    '''
    return message



def main() -> None:
    """Main function to handle user inputs and execute commands."""

    print(start())
    while True:

        command = input('>>> ').strip()

        if command.lower() in ("exit", "close", "goodbye", 'quit', 'q'):
            print("Good bye!")
            break

        args_list = command.split()

        if len(args_list) and (hands := args_list[0]) in handlers or (hands := ' '.join(args_list[:2])) in handlers:
            print(handlers[hands](args_list[len(hands.split()):]))
            save_users()
        else:
            print(f"{color('Enter one of the commands:', 'r')} {', '.join(list(handlers.keys()))}.")

    sys.exit(0)


handlers = {'add user': add_new_user,
            'remove user': remove_user,
            'add phone': add_phone,
            'change phone': change_phone,
            'show phone': show_phone,
            'remove phone': remove_phone,
            'add birthday': add_birthday,
            'change birthday': add_birthday,
            'show birthday': show_birthday,
            'when birthday': birthday_countdown,
            'remove birthday': remove_birthday,
            'find': find,
            'show all': show_all,
            'hello': hello,
            'help': manual
            }


if __name__ == '__main__':
    main()
