# Address Book
It is a simple address book application that allows users to manage their contacts, including adding users, adding phone numbers, adding birthdays, and searching for contacts. The program uses a command-line interface for interaction.

## Commands
- `add user <name> [phone1] [phone2] [birthday] ... `: Add a new user to the address book.
- `remove user <name>`: Deleting a user from the address book.
- `add phone <name> <phone1> [phone2] ... `: Add a phone number to an existing user.
- `change phone <name> <old_phone> <new_phone>`: Change a phone number of a user.
- `show phone <name>`: Show all phone numbers of a user.
- `remove phone <name> <phone1> [phone2] ... `: Deleting the phone number from an existing user.
- `add birthday <name> <date>`: Add a birthday to an existing user.
- `change birthday <name> <date>`: Change the birthday of a user.
- `show birthday <name>`: Show the birthday of a user.
- `when birthday <name>`: Show the number of days until the next birthday of a user.
- `remove birthday <name>`: Deleting date of birth from an existing user.
- `find <query>`: Search for users by part of their name or phone number.
- `show all`: Show all users in the address book.
- `hello`: Display a welcome message.
- `help`: Show the list of available commands.
- `save csv`: Additionally save all contacts in csv format.
- To exit the program, you can use one of the following commands: `exit`, `close`, `goodbye`, `quit`, or `q`.
### Note:
- Parameters enclosed in `<angle brackets>` and `[square brackets]` are placeholders that should be replaced with the actual values.
- Parameters enclosed in `<angle brackets>` are required and must be provided.
- Parameters enclosed in `[square brackets]` are optional and can be omitted.
- Name must not contain numbers.
- Phone numbers and birthdates should be entered without spaces in between the digits, allowing separators: .,-/_.
- The date should be in the format YYYY-MM-DD.