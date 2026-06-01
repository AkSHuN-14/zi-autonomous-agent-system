"""
Database Models and Setup
SQLite for development, with PostgreSQL support for production
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import os


@dataclass
class User:
    """User model for authentication"""
    id: int
    username: str
    email: str
    password_hash: str
    created_at: str
    is_active: bool = True
    role: str = "user"  # user, admin, trusted
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "role": self.role
        }


@dataclass
class AgentSession:
    """Agent execution session"""
    id: int
    user_id: int
    task: str
    status: str  # running, completed, failed, halted
    started_at: str
    completed_at: Optional[str]
    results: Optional[str]
    tokens_used: int
    cost: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task": self.task,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "tokens_used": self.tokens_used,
            "cost": self.cost,
            "results": json.loads(self.results) if self.results else None
        }


@dataclass
class ContentHistory:
    """Content generation history"""
    id: int
    user_id: int
    platform: str
    tone: str
    ucc_theme: str
    content: str
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "platform": self.platform,
            "tone": self.tone,
            "ucc_theme": self.ucc_theme,
            "content": self.content,
            "created_at": self.created_at
        }


class DatabaseManager:
    """
    Database Manager for production deployment
    Handles SQLite operations with PostgreSQL compatibility layer
    """
    
    def __init__(self, db_path: str = "data/agent_system.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.ensure_data_directory()
        self.initialize_database()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                role TEXT DEFAULT 'user'
            )
        """)
        
        # Agent sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                status TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                results TEXT,
                tokens_used INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Content history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                tone TEXT NOT NULL,
                ucc_theme TEXT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Security violations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                violation_type TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                description TEXT NOT NULL,
                detected_content TEXT,
                action_taken TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # API keys table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                key_hash TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, email: str, password: str, role: str = "user") -> User:
        """
        Create a new user
        
        Args:
            username: Username
            email: Email address
            password: Plain text password (will be hashed)
            role: User role
            
        Returns:
            Created user object
        """
        password_hash = self.hash_password(password)
        created_at = datetime.now().isoformat()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, created_at, role) VALUES (?, ?, ?, ?, ?)",
                (username, email, password_hash, created_at, role)
            )
            conn.commit()
            
            user_id = cursor.lastrowid
            return User(
                id=user_id,
                username=username,
                email=email,
                password_hash=password_hash,
                created_at=created_at,
                role=role
            )
        finally:
            conn.close()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    created_at=row["created_at"],
                    is_active=bool(row["is_active"]),
                    role=row["role"]
                )
            return None
        finally:
            conn.close()
    
    def verify_password(self, user: User, password: str) -> bool:
        """Verify password against hash"""
        return user.password_hash == self.hash_password(password)
    
    def hash_password(self, password: str) -> str:
        """Hash password (simplified - use bcrypt in production)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_agent_session(
        self,
        user_id: int,
        task: str,
        status: str = "running"
    ) -> AgentSession:
        """Create a new agent session"""
        started_at = datetime.now().isoformat()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO agent_sessions (user_id, task, status, started_at) VALUES (?, ?, ?, ?)",
                (user_id, task, status, started_at)
            )
            conn.commit()
            
            session_id = cursor.lastrowid
            return AgentSession(
                id=session_id,
                user_id=user_id,
                task=task,
                status=status,
                started_at=started_at,
                completed_at=None,
                results=None,
                tokens_used=0,
                cost=0.0
            )
        finally:
            conn.close()
    
    def update_agent_session(
        self,
        session_id: int,
        status: str,
        results: Optional[Dict[str, Any]] = None,
        tokens_used: int = 0,
        cost: float = 0.0
    ):
        """Update agent session"""
        completed_at = datetime.now().isoformat() if status in ["completed", "failed", "halted"] else None
        results_json = json.dumps(results) if results else None
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """UPDATE agent_sessions 
                   SET status = ?, completed_at = ?, results = ?, tokens_used = ?, cost = ?
                   WHERE id = ?""",
                (status, completed_at, results_json, tokens_used, cost, session_id)
            )
            conn.commit()
        finally:
            conn.close()
    
    def log_content_generation(
        self,
        user_id: int,
        platform: str,
        tone: str,
        ucc_theme: str,
        content: str
    ) -> ContentHistory:
        """Log content generation to database"""
        created_at = datetime.now().isoformat()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO content_history (user_id, platform, tone, ucc_theme, content, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, platform, tone, ucc_theme, content, created_at)
            )
            conn.commit()
            
            content_id = cursor.lastrowid
            return ContentHistory(
                id=content_id,
                user_id=user_id,
                platform=platform,
                tone=tone,
                ucc_theme=ucc_theme,
                content=content,
                created_at=created_at
            )
        finally:
            conn.close()
    
    def log_security_violation(
        self,
        user_id: Optional[int],
        violation_type: str,
        risk_level: str,
        description: str,
        detected_content: str,
        action_taken: str
    ):
        """Log security violation"""
        created_at = datetime.now().isoformat()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO security_violations 
                   (user_id, violation_type, risk_level, description, detected_content, action_taken, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, violation_type, risk_level, description, detected_content, action_taken, created_at)
            )
            conn.commit()
        finally:
            conn.close()
    
    def get_user_sessions(self, user_id: int, limit: int = 50) -> List[AgentSession]:
        """Get user's agent sessions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM agent_sessions WHERE user_id = ? ORDER BY started_at DESC LIMIT ?",
                (user_id, limit)
            )
            rows = cursor.fetchall()
            
            sessions = []
            for row in rows:
                sessions.append(AgentSession(
                    id=row["id"],
                    user_id=row["user_id"],
                    task=row["task"],
                    status=row["status"],
                    started_at=row["started_at"],
                    completed_at=row["completed_at"],
                    results=row["results"],
                    tokens_used=row["tokens_used"],
                    cost=row["cost"]
                ))
            return sessions
        finally:
            conn.close()
    
    def get_content_history(self, user_id: int, limit: int = 50) -> List[ContentHistory]:
        """Get user's content generation history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM content_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit)
            )
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                history.append(ContentHistory(
                    id=row["id"],
                    user_id=row["user_id"],
                    platform=row["platform"],
                    tone=row["tone"],
                    ucc_theme=row["ucc_theme"],
                    content=row["content"],
                    created_at=row["created_at"]
                ))
            return history
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            stats = {}
            
            # User count
            cursor.execute("SELECT COUNT(*) as count FROM users")
            stats["total_users"] = cursor.fetchone()["count"]
            
            # Session count
            cursor.execute("SELECT COUNT(*) as count FROM agent_sessions")
            stats["total_sessions"] = cursor.fetchone()["count"]
            
            # Content generation count
            cursor.execute("SELECT COUNT(*) as count FROM content_history")
            stats["total_content_generated"] = cursor.fetchone()["count"]
            
            # Security violations count
            cursor.execute("SELECT COUNT(*) as count FROM security_violations")
            stats["total_violations"] = cursor.fetchone()["count"]
            
            # Token usage
            cursor.execute("SELECT SUM(tokens_used) as total FROM agent_sessions")
            result = cursor.fetchone()
            stats["total_tokens_used"] = result["total"] or 0
            
            # Cost
            cursor.execute("SELECT SUM(cost) as total FROM agent_sessions")
            result = cursor.fetchone()
            stats["total_cost"] = result["total"] or 0.0
            
            return stats
        finally:
            conn.close()


# Authentication Manager
class AuthenticationManager:
    """
    Authentication and authorization management
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize authentication manager
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
        self.current_user: Optional[User] = None
    
    def register_user(self, username: str, email: str, password: str, role: str = "user") -> User:
        """Register a new user"""
        return self.db_manager.create_user(username, email, password, role)
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate user"""
        user = self.db_manager.get_user_by_username(username)
        
        if user and self.db_manager.verify_password(user, password):
            self.current_user = user
            return True
        
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Get currently authenticated user"""
        return self.current_user
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def is_authorized(self, required_role: str) -> bool:
        """Check if current user has required role"""
        if not self.current_user:
            return False
        
        role_hierarchy = {
            "user": 0,
            "trusted": 1,
            "admin": 2
        }
        
        user_level = role_hierarchy.get(self.current_user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def is_trusted_entity(self, username: str) -> bool:
        """Check if username is a trusted entity (TA'K$HUN criteria)"""
        trusted_entities = ["TA'K", "TA'K$HUN", "TAK$SHUN", "Ta'K", "Ta'K$HuN"]
        return username in trusted_entities or username.lower() in [e.lower() for e in trusted_entities]


# Initialize production database
def initialize_production_database(db_path: str = "data/agent_system.db") -> DatabaseManager:
    """Initialize production database with default admin user"""
    db_manager = DatabaseManager(db_path)
    auth_manager = AuthenticationManager(db_manager)
    
    # Create default admin user if not exists
    admin_user = db_manager.get_user_by_username("admin")
    if not admin_user:
        auth_manager.register_user("admin", "admin@rellyvent.com", "admin123", role="admin")
        print("Created default admin user: admin / admin123")
    
    # Create TA'K$HUN trusted user if not exists
    tak_user = db_manager.get_user_by_username("TA'K$HUN")
    if not tak_user:
        auth_manager.register_user("TA'K$HUN", "tak@rellyvent.com", "tak123", role="trusted")
        print("Created TA'K$HUN trusted user: TA'K$HUN / tak123")
    
    return db_manager


if __name__ == "__main__":
    # Initialize database
    db_manager = initialize_production_database()
    
    # Test database operations
    print("Database Statistics:")
    stats = db_manager.get_statistics()
    print(json.dumps(stats, indent=2))
