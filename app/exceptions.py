class NotSufficientFounds(Exception):
    pass


class AccountNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class SameAccounts(Exception):
    pass


class UserAlreadyIn(Exception):
    message = "user already in"
