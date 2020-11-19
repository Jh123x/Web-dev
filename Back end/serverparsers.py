import os
import sqlite3


class Database(object):
    def __init__(self, dbpath: str, name: str):
        """Base database object"""
        # Store the name
        self.name = name

        # Store the database path
        self.dbpath = dbpath

        # Connect to the database
        self.connection = sqlite3.connect(dbpath, timeout=10)

        # Get the cursor of the database
        self.cursor = self.connection.cursor()

        # Cache
        self.cache = []
        self.changed = True

    def execute(self, command: str, *args) -> None:
        """Execute the SQL command in the form of a string"""

        # Run the command
        self.cursor.execute(command, *args)

    def is_cache(self) -> bool:
        """Check if there is a cached copy of the database"""
        return True if self.cache else False

    def fetch_all(self) -> tuple:
        """Fetch all the data from the table"""

        # If there is no cache or if there are changes in the cache
        if self.changed or not self.is_cache():
            # Fetch all the items in the table and add it to the cache
            self.cursor.execute(f"SELECT * FROM {self.name}", )
            self.cache = self.cursor.fetchall()

            # Make the changes as none
            self.changed = False

        # Return the items
        return self.cache

    def __del__(self):
        """Destructor for the Scoreboard
            Commits all the changes that is done
        """
        # Save all changes
        self.connection.commit()


class CRUDDatabase(Database):
    def __init__(self, db_path:str):
        """Database object to store CRUD operations for Web"""
        self.name = 'crud'
        #Call the superclass obj
        super().__init__(db_path, self.name)

        # Create the table if it does not exist
        self.execute(f"CREATE TABLE IF NOT EXISTS {self.name} (id INTEGER, key TEXT, value TEXT)")

    def add(self, key: str, value: str) -> None:
        """Add the settings to the table"""
        # Insert the element into the table
        self.execute(f'INSERT INTO {self.name} VALUES(?, ?, ?)', (None, key, value))

        # Mark the database as changed
        self.changed = True

    def update(self, key: str, value: str) -> None:
        """Update the value of the settings"""
        # Call the update function

        # print(settings)
        self.execute(f"UPDATE {self.name} SET value = ? WHERE key = ?", (value, key))

        # Mark db as changed
        self.changed = True

    def remove(self, key: str) -> None:
        """Remove the last entry from the highscore board"""
        # Remove from the database where the name matches the name to be removed
        self.execute(f"DELETE FROM {self.name} WHERE key = ?", (key,))

        # Mark the database as changed
        self.changed = True

    def get(self, key: str) -> str:
        self.execute(f"SELECT * FROM {self.name} WHERE key = ?", (key,))
        rows = self.cursor.fetchall()
        if(len(rows) == 0):
            return None
        return rows[0][2]
        


class WebParser(object):
    def __init__(self, dbpath:str):
        """Main object for WebParser"""
        self.parsers = {
            "generic" : self.handle_generic,
            "name" : self.handle_name,
            "get" : self.handle_get,
            "update" : self.handle_update,
            "post" : self.handle_post,
            "remove": self.handle_remove
        }
        self.db = CRUDDatabase(dbpath)
        self.error_msg = """404 Data is not found"""


    def handle_remove(self, data:dict):
        """Handle the removal method"""
        key = data.get('key', None)

        if (key == None or self.db.get(key) == None):
            return self.error_msg

        self.db.remove(key)
        return f"Key {key} removed successfully"
    

    def handle_update(self, data:dict):

        #Get the appropriate values
        key = data.get('key', None)
        value = data.get('value', None)

        #If either the key or value is none, return error message
        if(key == None or value == None):
            return self.error_msg

        #Otherwise update the data
        self.db.update(key, value)

        #Return update message
        return f"Data updated {(key, value)}"

    def handle_post(self, data:dict):
        #Get the appropriate values
        key = data.get('key', None)
        value = data.get('value', None)

        #If either the key or value is none, return error message
        if(key == None or value == None):
            return self.error_msg

        #Otherwise update the data
        self.db.add(key, value)

        #Return update message
        return f"Data added {(key, value)}"

    def handle_get(self, data:dict):
        #Check if the data is none
        key = data.get("key", None)
        value = self.db.get(key)
        #Check if the key is none
        if(key == None or value == None):
            return self.error_msg
        
        #Data retrieved
        return f"Data received {value}"

    def handle_name(self, data:dict):
        """Handle the name of the person in the form"""
        firstname = data['fname']
        lastname = data['lname']
        return f"""<b>Hello {firstname} {lastname}</b>"""

    def handle_generic(self, data:dict):
        """Handle the generic case"""

        return f"""<b>Error Protocol not found</b>"""

    def parse(self, data:dict) -> str:
        """Parse the data to json"""
        handler_type = data.get("type", "").lower()
        handler = self.parsers.get(handler_type, self.parsers["generic"])
        result = handler(data)
        # print(result)
        return result
