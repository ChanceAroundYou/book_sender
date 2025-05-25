class BookSeries:
    """书籍系列枚举"""

    ECONOMIST_USA = "economist_usa"
    ECONOMIST_EUROPE = "economist_europe"
    ECONOMIST_ASIA = "economist_asia"
    ECONOMIST_UK = "economist_uk"
    ECONOMIST_ME_AFRICA = "economist_me_africa"
    OTHER = ""

    @classmethod
    def get_series(cls, title: str) -> str:
        """获取书籍系列"""
        title = title.lower()
        if "economist" in title:
            if "usa" in title:
                return cls.ECONOMIST_USA
            elif "europe" in title:
                return cls.ECONOMIST_EUROPE
            elif "asia" in title:
                return cls.ECONOMIST_ASIA
            elif "uk" in title:
                return cls.ECONOMIST_UK
            elif "africa" in title:
                return cls.ECONOMIST_ME_AFRICA
        return cls.OTHER

    @classmethod
    def check_series(cls, series: str) -> bool:
        """检查系列是否存在"""
        return series in cls.get_series_list()

    @classmethod
    def get_series_list(cls) -> list:
        """获取所有系列列表"""
        return [
            value
            for name, value in vars(cls).items()
            if not name.startswith("_")
            and not callable(value)
            and not isinstance(value, classmethod)
        ]

    @classmethod
    def simplify_series(cls, series: str) -> str:
        """简化系列"""
        if "economist" in series:
            return "economist"
        else:
            return series
