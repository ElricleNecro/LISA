#!/usr/bin/env python3

import pandas as pd

from querier import Querier
from sqlalchemy import create_engine


class ReadSQL(object):

    """
    A class to read data easily in a SQL database.
    """

    def __init__(self, database, querier=Querier()):
        """
        Store the informations of the database.
        """

        self.database = database
        self.querier = querier

    @property
    def database(self):

        return self._database

    @property
    def querier(self):

        return self._querier

    @database.setter
    def database(self, database):

        self._database = database
        self._conn = create_engine("sqlite:///{0}".format(self._database))

    @querier.setter
    def querier(self, querier):

        self._querier = querier

    def __call__(self, **kwargs):
        """
        When calling the instance, executes
        a query passing arguments in keyword fashion
        to the query instance which creates a SQL query
        with its argument. The querier instance can be
        set with the ReadSQL instance.
        """

        # reformat select statement
        select = kwargs["select"].split(",")
        kwargs.pop("select", None)

        # the query
        query = self._querier(*select, **kwargs)

        # return the query into a DataFrame
        return pd.read_sql(
            query,
            self._conn,
        )
