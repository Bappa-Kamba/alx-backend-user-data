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
        """
        Memoized session object
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

    def find_user_by(self, **kwargs) -> User:
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
            raise NoResultFound('No result found')
        except InvalidRequestError:
            raise InvalidRequestError('Invalid request')

    def update_user(self, user_id: int, **kwargs) -> None:
        """
            Updates a user by id

            Args:
                user_id: The id of the user to update
                kwargs: The key word arguments to update the user with

            Returns:
                None

            Raises:
                ValueError: If an invalid attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
            for attr, value in kwargs.items():
                if hasattr(user, attr):
                    setattr(user, attr, value)
                else:
                    raise ValueError(f'Invalid attribute {attr}')
            self._session.commit()
        except ValueError as e:
            self._session.rollback()
            print(e)
