from typing import List


class Role:
    LAWYER = "Lawyer"
    ECONOMIST = "Economist"
    GENERAL_DIRECTOR = "General director"

    @classmethod
    def get_roles(cls) -> List[str]:
        return [cls.LAWYER, cls.ECONOMIST, cls.GENERAL_DIRECTOR]
