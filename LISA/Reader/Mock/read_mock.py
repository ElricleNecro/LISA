#!/usr/bin/env python3

import pandas as pd

from .read_sql import ReadSQL


class ReadMock(object):
    """
    A class to read data from the mock catalog of galaxies.
    """

    def __init__(self, database, old=False):
        """
        A class to read data from the mock catalog of galaxies.

        :params database: the path to the database containing the mock
            catalogue data.
        :params old: a parameter to make the class compatible with old
            versions of the mock catalogue structure.
        """
        self.database = database
        self.old = old

    @property
    def database(self):
        return self._database

    @property
    def old(self):
        return self._old

    @property
    def left_on(self):
        return self._left_on

    @property
    def right_on(self):
        return self._right_on

    @left_on.setter
    def left_on(self, left_on):
        if left_on is not None:
            self._left_on = left_on

    @right_on.setter
    def right_on(self, right_on):
        if right_on is not None:
            self._right_on = right_on

    @database.setter
    def database(self, database):
        self._database = database

        # set the SQL object for the connection
        self._sql = ReadSQL(database)

    @old.setter
    def old(self, old):
        self._old = old
        if old:
            self._left_on = "indexx"
            self._right_on = "index"
        else:
            self._left_on = "galaxyid"
            self._right_on = "galaxyID"

    def __call__(self, **kwargs):
        """
        To select data from the SQL database containing galaxies.
        Just need to pas as keyword arguments the different fields
        needed for an SQL query as for example "select", "where"; etc...
        Returns a DataFrame containing the different fields with filtration
        specified in "select".
        """

        # add the table from which to read
        kwargs.update({"from": "MOCK"})

        # return data
        return self._sql(**kwargs)

    def get_true_groups(self, galaxies):
        """
        To extract halos in real space from the identity
        of the unique group identity. Galaxies must be
        extracted from the mock catalog.
        """

        return galaxies.groupby("group_id")

    def join_snapshot(
        self,
        galaxies,
        snapshot,
        left_on=None,
        right_on=None,
    ):
        """
        A function to do the join between galaxies in the mock
        catalog and galaxies in the snapshot used to construct
        the mock catalog.
        """

        # compatibility with old versions of the mock catalog
        self.left_on = left_on
        self.right_on = right_on

        return pd.merge(
            galaxies,
            snapshot,
            left_on=self.left_on,
            right_on=self.right_on,
        )

# vim: set tw=79 :
