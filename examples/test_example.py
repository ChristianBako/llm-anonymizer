"""Example Python code to test anonymization."""

class DatabaseManager:
    def __init__(self, connection_string: str, max_connections: int = 10):
        self.connection_string = connection_string
        self.max_connections = max_connections
        self.active_connections = []
        
    def connect_to_database(self):
        """Establishes connection to the database."""
        if len(self.active_connections) >= self.max_connections:
            raise Exception("Maximum connections reached")
            
        # Create new connection
        connection = self._create_connection()
        self.active_connections.append(connection)
        return connection
        
    def _create_connection(self):
        """Private method to create database connection."""
        import sqlite3
        return sqlite3.connect(self.connection_string)
        
    def execute_query(self, query: str, parameters: tuple = ()):
        """Execute SQL query with parameters."""
        connection = self.connect_to_database()
        cursor = connection.cursor()
        
        try:
            result = cursor.execute(query, parameters)
            return result.fetchall()
        finally:
            connection.close()


def main():
    db_manager = DatabaseManager("example.db")
    users = db_manager.execute_query("SELECT * FROM users WHERE age > ?", (18,))
    print(f"Found {len(users)} adult users")


if __name__ == "__main__":
    main()