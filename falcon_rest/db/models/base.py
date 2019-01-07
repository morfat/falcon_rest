
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Boolean,DateTime,Date,ForeignKey,Numeric,UniqueConstraint, Float
from falcon_rest.utils import timestamp_uuid

import datetime

def StringField(length,*args,**kwargs):
    return Column(String(length),*args,**kwargs)

def DateTimeField(*args,**kwargs):
    return Column(DateTime,*args,**kwargs)

def CreatedAtField(*args,**kwargs):
    return DateTimeField(nullable = False,default = datetime.datetime.utcnow)

def UpdatedAtField(*args,**kwargs):
    return DateTimeField(nullable = False,default = datetime.datetime.utcnow,onupdate = datetime.datetime.utcnow)

def DateField(*args,**kwargs):
    return Column(Date,*args,**kwargs)
 

def BooleanField(*args,**kwargs):
    return Column(Boolean,*args,**kwargs)

def IntegerField(*args,**kwargs):
    return Column(Integer,*args,**kwargs)

def DecimalField(precision,scale,*args,**kwargs):
    #precision => max_digits and scale=> decimal places
    return Column(Numeric(precision = precision, scale = scale),*args,**kwargs)

def FloatField(*args,**kwargs):
    return Column(Float,*args,**kwargs)

def UniqueTogether(*args,**kwargs):
    return UniqueConstraint(*args,**kwargs)

def AutoPrimaryKeyField():
    return StringField(50, primary_key=True, default=timestamp_uuid)

def ForeignKeyField(references,*args,**kwargs):
    return StringField(50,ForeignKey(references),*args, **kwargs)


"""
class BaseTable:
    pass
    

Base = declarative_base(cls = BaseTable)
"""

Base = declarative_base()
