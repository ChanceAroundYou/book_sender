class BookCategory:
    """书籍分类枚举"""
    ECONOMIST = "economist"
    ECONOMIST_USA = "economist_usa"
    ECONOMIST_EUROPE = "economist_europe"
    ECONOMIST_ASIA = "economist_asia"
    ECONOMIST_UK = "economist_uk"
    ECONOMIST_ME_AFRICA = "economist_me_africa"
    OTHER = "other"

    @classmethod
    def get_category(cls, title: str) -> str:
        """获取书籍分类"""
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
            else:
                return cls.ECONOMIST
        return cls.OTHER
    
    @classmethod
    def check_category(cls, category: str) -> bool:
        """检查分类是否存在"""
        return category in cls.get_categories()
    
    @classmethod
    def get_categories(cls) -> list:
        """获取所有分类列表"""
        return [value for name, value in vars(cls).items()
                if not name.startswith('_') and not callable(value) 
                and not isinstance(value, classmethod)]
    
    @classmethod
    def simplify_category(cls, category: str) -> str:
        """简化分类"""
        if 'economist' in category:
            return 'economist'
        else:
            return category
