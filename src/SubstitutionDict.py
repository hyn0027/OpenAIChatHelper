class SubstitutionDict(dict):
    """Dict where key and value must be string. Dynamic checking enforced"""

    def __setitem__(self, key: str, value: str) -> None:
        if type(key) != str:
            raise ValueError("key must be a string")
        if type(value) != str:
            raise ValueError("value must be a string")
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> str:
        if type(key) != str:
            raise ValueError("key must be a string")
        return super().__getitem__(key)