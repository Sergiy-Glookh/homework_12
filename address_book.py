from collections import UserDict
from datetime import datetime
from exceptions import *

N = 10


class Field:
    """Base class for fields in a record."""

    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    @staticmethod
    def valid_value(value: str) -> bool:
        if value:
            return True
        return False

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, val: str) -> None:
        if self.valid_value(val):
            self.__value = val


class Name(Field):
    """Name field in a record."""


class Phone(Field):
    """Phone number field in a record."""

    @staticmethod
    def valid_value(value: str) -> bool:
        phone = ''.join(filter(str.isdigit, value))
        if 8 < len(phone) < 13 and len(value) < 20:
            return True


class Birthday(Field):
    """Birthday field in a record."""

    @staticmethod
    def valid_value(birthday: datetime) -> bool:
        if isinstance(birthday, datetime) and 0 < datetime.now().year - birthday.year <= 100:
            return True
        else:
            raise InvalidBirthday


class Record:
    """Record representing a contact in the address book."""

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        """
        Initialize a new record.

        Args:
            name (Name): The name of the contact.
            phone (Phone, optional): The phone number of the contact. Defaults to None.
        """

        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def days_to_birthday(self) -> int | None:
        """
        Calculate the number of days until the next birthday.

        Returns:
            int or None: The number of days until the next birthday, or None if the birthday is not set.
        """

        if self.birthday:
            current_date = datetime.now()
            celebration_birthday = datetime(current_date.year, self.birthday.value.month, self.birthday.value.day)
            if current_date > celebration_birthday:
                celebration_birthday = datetime(current_date.year + 1, self.birthday.value.month, self.birthday.value.day)

            return (celebration_birthday - current_date).days

        return None

    @input_error
    def add_birthday(self, birthday: Birthday) -> str:
        """
        Add a date of birth to the record.

        Args:
            birthday (Birthday): The birthday to add.
        """

        if not self.birthday:
            raise InvalidBirthday

        if birthday.value == self.birthday.value:
            raise AddingExistingBirthday

        if birthday.value:
            self.birthday = birthday

        return "Birthday added successfully."

    def remove_birthday(self) -> None:
        """Remove the birthday from the record."""

        self.birthday = None

    @input_error
    def add_phone(self, phone: Phone) -> str:
        """
        Add a phone number to the record.

        Args:
            phone (Phone): The phone number to add.
        """

        for existing_phone in self.phones:
            if existing_phone.value == phone.value:
                raise AddingExistingPhone

        if phone.value:
            self.phones.append(phone)
        else:
            raise InvalidPhoneNumber

        return "Phone number added successfully."

    @input_error
    def remove_phone(self, phone: Phone) -> str | None:
        """
        Remove a phone number from the record.

        Args:
            phone (Phone): The phone number to remove.
        """

        for existing_phone in self.phones:
            if phone.value == existing_phone.value:
                self.phones.remove(existing_phone)
                return "Phone number deleted successfully."

        return "The user does not have such a phone number"

    @input_error
    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str | None:
        """
        Edit a phone number in the record.

        Args:
            old_phone (Phone): The old phone number to replace.
            new_phone (Phone): The new phone number.
        """

        if not new_phone.value:
            raise InvalidPhoneNumber
        for idx, phone in enumerate(self.phones):
            if old_phone.value == phone.value:
                self.phones[idx] = new_phone
                return "The phone number has been changed successfully."

        return "The user does not have such a phone number"


class AddressBook(UserDict):
    """Address book that extends UserDict."""

    def __init__(self) -> None:
        """Initialize an address book."""
        super().__init__()

    def add_record(self, record: Record) -> None:
        """
        Add a record to the address book.

        Args:
            record (Record): The record to add.
        """

        self.data[record.name.value] = record

    def search(self, search_substr: str) -> str:  # AddressBook | str:
        """
        Find a name by phone or a phone with a name in the address book.

        Args:
            search_substr: The search object representing either a Name or a Phone.

        Returns:
            Optional: The search results. If searching by Name, returns a list of phone numbers.
                If searching by Phone number, returns the name of the contact. Returns None if no match is found.
        """

        found_users = AddressBook()
        for name, rec in self.data.items():
            if search_substr in name:
                found_users[name] = rec
                continue
            for phone in rec.phones:
                if search_substr in phone.value:
                    found_users[name] = rec
                    continue
        if found_users:
            return found_users

        return "Nothing was found for your request"

    def __iter__(self):
        self.keys_iter = iter(self.data)
        return self

    def __next__(self, n: int = N) -> str:
        """
        Get the next batch of records as a string representation.

        Args:
            n (int, optional): The number of records to retrieve. Defaults to N.

        Returns:
            str: The string representation of the next batch of records.
        """

        items = []
        try:
            for _ in range(n):
                key = next(self.keys_iter)
                items.append((key, self.data[key]))
        except StopIteration:
            if not items:
                raise StopIteration

        representation_record = '-' * 70 + '\n'
        representation_record += '|{:^33}|{:^20}|{:^13}|\n'.format("User", "Phones", "Birthday")
        representation_record += '-' * 70 + '\n'
        for name, user in sorted(items):
            birthday = user.birthday.value.strftime("%d.%m.%Yp") if user.birthday else ''
            for i in range(len(user.phones)):
                if i == 0:
                    representation_record += '| {:<32}|{:>19} |{:^13}|\n'.format(name, user.phones[i].value, birthday)
                else:
                    representation_record += '|{:<33}|{:>19} |{:^13}|\n'.format(' ', user.phones[i].value, ' ')
            if not user.phones:
                representation_record += '| {:<32}|{:>19} |{:^13}|\n'.format(name, ' ', birthday)
            representation_record += '-' * 70 + '\n'

        return representation_record
