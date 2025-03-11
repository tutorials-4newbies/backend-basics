import datetime
from peewee import SqliteDatabase, Model, CharField, DateTimeField, BooleanField

# create a peewee database instance -- our models will use this database to
# persist information
database = SqliteDatabase("local.db")

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database

class Task(BaseModel):
    name = CharField()
    is_completed = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)


def create_tables():
    with database:
        database.create_tables([Task])