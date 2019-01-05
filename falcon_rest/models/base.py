
from sqlalchemy.ext.declarative import declarative_base

class BaseTable:
    pass
    

Base = declarative_base(cls = BaseTable)