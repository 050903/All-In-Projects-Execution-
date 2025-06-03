from datetime import datetime

class SessionManager:
    def __init__(self):
        self.current_session = None
        self.sessions = {}
    
    def create_session(self, user_id):
        """Create a new session for a user"""
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.sessions[session_id] = {
            'user_id': user_id,
            'start_time': datetime.now(),
            'status': 'active',
            'data': {}
        }
        self.current_session = session_id
        return session_id
    
    def get_session(self, session_id):
        """Retrieve a session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id, data):
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id]['data'].update(data)
            return True
        return False
    
    def end_session(self, session_id):
        """End a session"""
        if session_id in self.sessions:
            self.sessions[session_id]['status'] = 'completed'
            self.sessions[session_id]['end_time'] = datetime.now()
            if self.current_session == session_id:
                self.current_session = None
            return True
        return False