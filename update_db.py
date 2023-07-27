import json
import os
import sqlite3


class TalkToDb:
    DB_NAME = 'dota.db'

    def __init__(self, clear_db=False):
        self.conn = sqlite3.connect(self.DB_NAME)
        if clear_db:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]};")
            self.conn.commit()

    def check_if_database_exists(self):
        if not os.path.exists(self.DB_NAME):
            return False
        if os.stat(self.DB_NAME).st_size == 0:
            return False
        return True

    def init_heroes_table(self):
        cursor = self.conn.cursor()

        drop_table_query = f"DROP TABLE IF EXISTS heroes"
        cursor.execute(drop_table_query)

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS heroes (
            hero_id INTEGER PRIMARY KEY,
            name TEXT,
            localized_name TEXT,
            primary_attr TEXT,
            attack_type TEXT,
            role TEXT
        )
        '''

        # Execute the create table query
        cursor.execute(create_table_query)

        # Commit the changes and close the connection
        self.conn.commit()

    def init_matches_table(self):
        cursor = self.conn.cursor()

        drop_matches_query = f"DROP TABLE IF EXISTS matches"
        cursor.execute(drop_matches_query)

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS heroes (
            hero_id INTEGER PRIMARY KEY,
            name TEXT,
            localized_name TEXT,
            primary_attr TEXT,
            attack_type TEXT,
            role TEXT
        )
        '''

        # Execute the create table query
        cursor.execute(create_table_query)

        # Commit the changes and close the connection
        self.conn.commit()

    def update_one_hero_data(self, one_hero_data):
        cursor = self.conn.cursor()
        hero_id = one_hero_data.get('id')
        name = one_hero_data.get('name')
        localized_name = one_hero_data.get('localized_name')
        primary_attr = one_hero_data.get('primary_attr')
        attack_type = one_hero_data.get('attack_type')
        roles = one_hero_data.get('roles')
        roles_str = ', '.join(roles) if roles else None
        update_query = '''
        INSERT INTO heroes (hero_id, name, localized_name, primary_attr, attack_type, role)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(update_query, (hero_id, name, localized_name, primary_attr, attack_type, roles_str))
        self.conn.commit()


if __name__ == "__main__":
    talk_db = TalkToDb(clear_db=True)
    talk_db.init_matches_table()
