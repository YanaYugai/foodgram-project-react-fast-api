from sqlalchemy import Integer, ForeignKey, String, Table, Column, MetaData

metadata = MetaData()

users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True),
              Column('username', String(50), nullable=False),
              Column('email', String(50), nullable=False),
              Column('first_name', String(50), nullable=False),
              Column('last_name', String(50), nullable=False),
              Column('password', String(50), nullable=False),)
