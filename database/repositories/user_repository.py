from ..interfaces import IUserRepository, ISQLOperations


class UserRepository(IUserRepository):
    def __init__(self, db: ISQLOperations):
        self.db = db

    def get_user(self, username: str):
        query = "SELECT * FROM users WHERE nombre = ?"
        user = self.db.execute_query(query, (username,))[0]
        
        return user[0] if user else None
        

    def create_user(
        self,
        username: str,
        password: str,
        role: str,
        telefono: str,
        email: str,
        direccion: str,
    ):
        query = "INSERT INTO users (nombre, password, role, telefono, email, direccion) VALUES (?, ?, ?, ?, ?, ?)"
        params = (username, password, role, telefono, email, direccion)
        self.db.execute_query(query, params)
        return self.get_user

    def create_default_users(self):
        admin_exists = self.get_user("admin")
        user_exists = self.get_user("user")
        
        if not admin_exists:
            query = "INSERT INTO users (nombre, password, role) VALUES (?, ?, ?)"
            params = ("admin", "admin", "admin")
            self.db.execute_query(query, params)

        if not user_exists:
            query = "INSERT INTO users (nombre, password, role) VALUES (?, ?, ?)"
            params = ("user", "user", "cliente")
            self.db.execute_query(query, params)


    def listar_usuarios(self, role=None):
        query = "SELECT * FROM users"
        if role:
            query += " WHERE role = ?"
            params = (role,)
        users = self.db.execute_query(query, params)
        return users[0]
    
    