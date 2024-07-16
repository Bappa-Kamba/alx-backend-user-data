#!/usr/bin/env python3
""" Databse Configuration Module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User, Base

class DB:
    """ DB Class """

    def __init__(self) -> None:
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Adds a user to the database
            Args:
                email: The email of the user
                hashed_password: The hashed password of the user
            Returns:
                The new user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user
    
    def find_user_by(self, **kwargs):
        """
            Finds a user by key word arguments

            Args:
                kwargs: The key word arguments

            Returns:
            The first user found that matches the criteria.

            Raises:
                NoResultFound: If no user is found with the given criteria.
                InvalidRequestError: If the request is invalid.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound('Not found')
        except InvalidRequestError:
            raise InvalidRequestError('Invalid')


my_db = DB()

user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
