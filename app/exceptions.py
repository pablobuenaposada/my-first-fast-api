class NotSufficientFounds(Exception):
    message = f"account doesn't have sufficient founds"


class AccountNotFound(Exception):
    message = "account not found"


class UserNotFound(Exception):
    message = "user not found"


class SameAccounts(Exception):
    message = "origin and destination accounts (emails) are the same"


class UserAlreadyIn(Exception):
    message = "user already in"
