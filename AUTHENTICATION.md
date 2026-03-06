# TerraFoma Authentication System

## Overview

TerraFoma now features a complete role-based authentication system that separates **Landowners** and **Business** users, providing each with tailored experiences.

## User Roles

### 🌳 Landowner
- **Purpose**: Sell carbon credits from their land
- **Access**: Registry, Marketplace, Homepage, Scan Land
- **Features**:
  - Scan land plots using AI satellite analysis
  - Generate carbon credits
  - List credits on marketplace
  - View registry of all credits

### 🏭 Business / Industrial
- **Purpose**: Buy carbon credits to offset emissions
- **Access**: Registry, Marketplace, Homepage, Dashboard
- **Features**:
  - View emissions dashboard with IEA data
  - Calculate carbon footprint
  - Browse and purchase carbon credits
  - Track transaction history

## Architecture

### Frontend Components

#### 1. **AuthContext** (`/src/contexts/AuthContext.tsx`)
- Manages authentication state globally
- Provides hooks: `useAuth()`
- Methods: `login()`, `signup()`, `logout()`
- Stores user session in localStorage

#### 2. **ProtectedRoute** (`/src/components/ProtectedRoute.tsx`)
- Wraps protected pages to enforce authentication
- Redirects unauthorized users to login
- Role-based route protection
- Shows loading state during auth checks

#### 3. **Updated Navbar** (`/src/components/Navbar.tsx`)
- Dynamically shows links based on user role
- Displays user profile dropdown when authenticated
- Shows Login/Signup buttons when not authenticated
- Role badge in user menu

#### 4. **Auth Pages**
- **Login** (`/app/login/page.tsx`): Email/password authentication
- **Signup** (`/app/signup/page.tsx`): Registration with role selection

### Backend API

#### Auth Router (`/backend/routers/auth.py`)

**Endpoints:**

```
POST /api/auth/signup
- Create new account with role selection
- Body: { email, password, full_name, role, company_name? }
- Returns: { user, token }

POST /api/auth/login
- Authenticate with email/password
- Body: { email, password }
- Returns: { user, token }

POST /api/auth/logout
- Invalidate session token
- Body: { token }

GET /api/auth/me?token={token}
- Get current user from token
- Returns: user object
```

### Database Schema

#### Updated Tables

**users** table:
```sql
- id (UUID)
- email (TEXT, unique)
- password_hash (TEXT) -- NEW
- full_name (TEXT)
- role (TEXT) -- 'landowner' | 'business' | 'admin'
- company_name (TEXT, optional)
- created_at (TIMESTAMPTZ)
```

**sessions** table (NEW):
```sql
- id (UUID)
- user_id (UUID -> users.id)
- token (TEXT, unique)
- created_at (TIMESTAMPTZ)
- expires_at (TIMESTAMPTZ, default 30 days)
```

## Setup Instructions

### 1. Database Migration

Run the migration to add authentication support:

```bash
# In Supabase SQL Editor or via CLI
psql -f backend/data/migration_add_auth.sql
```

Or copy the contents of `backend/data/migration_add_auth.sql` into Supabase SQL Editor.

### 2. Environment Variables

Ensure you have these in your `.env.local` (frontend):
```
NEXT_PUBLIC_API_URL=http://localhost:8002
```

### 3. Start Servers

```bash
# Backend
cd backend
source ../.venv/bin/activate
uvicorn main:app --reload --port 8002

# Frontend
cd frontend
npm run dev
```

### 4. Test Authentication

1. Visit http://localhost:3001
2. Click "Sign up"
3. Choose role (Landowner or Business)
4. Fill form and create account
5. Verify navigation shows correct links for your role

## User Flow

### Landowner Flow
```
1. Visit homepage → Click "I'm a Landowner"
2. Sign up with role=landowner
3. Redirected to homepage (authenticated)
4. Navbar shows: Home, Registry, Marketplace, Scan Land
5. Click "Scan Land" to create carbon credits
6. Draw polygon, run AI scan, accept contract
7. Credit appears in Registry and Marketplace
```

### Business Flow
```
1. Visit homepage → Click "I'm a Business"
2. Sign up with role=business
3. Redirected to homepage (authenticated)
4. Navbar shows: Home, Registry, Marketplace, Dashboard
5. Click "Dashboard" to see emissions data
6. Calculate carbon footprint
7. Browse Marketplace to purchase credits
8. Complete transaction to offset emissions
```

## Security Notes

⚠️ **Current Implementation** (Hackathon/Demo):
- Uses SHA256 password hashing
- Bearer tokens stored in localStorage
- Session tokens expire after 30 days
- No email verification

🔒 **Production Recommendations**:
- Use `bcrypt` or `argon2` for password hashing
- Implement JWT with refresh tokens
- Add HTTP-only cookies instead of localStorage
- Enable HTTPS/TLS
- Add email verification
- Implement rate limiting on auth endpoints
- Add 2FA support
- Use OAuth providers (Google, GitHub)

## API Integration

To authenticate API calls, include the token:

```typescript
const token = localStorage.getItem('terrafoma_token');

fetch(`${API_URL}/api/protected-endpoint`, {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
```

## Testing

### Create Test Users

```sql
-- Landowner
INSERT INTO users (email, password_hash, full_name, role) VALUES
('landowner@test.com', 'hashed_password', 'John Farmer', 'landowner');

-- Business
INSERT INTO users (email, password_hash, full_name, role, company_name) VALUES
('business@test.com', 'hashed_password', 'Jane CEO', 'business', 'Green Corp');
```

### Manual Test Checklist

- [ ] Signup as landowner
- [ ] Login as landowner
- [ ] Verify "Scan Land" link appears
- [ ] Verify "Dashboard" link hidden
- [ ] Logout
- [ ] Signup as business
- [ ] Login as business
- [ ] Verify "Dashboard" link appears
- [ ] Verify "Scan Land" link hidden
- [ ] Test protected route redirect
- [ ] Test user menu dropdown
- [ ] Test logout functionality

## Troubleshooting

**Issue**: "Failed to create account"
- Check backend logs for detailed error
- Verify database connection
- Ensure migration was run

**Issue**: Protected routes not working
- Clear localStorage: `localStorage.clear()`
- Check browser console for errors
- Verify token is being stored

**Issue**: Navigation links not updating
- Hard refresh page (Cmd+Shift+R)
- Check user role in user menu
- Verify Navbar is reading auth context correctly

## Future Enhancements

- [ ] Email verification
- [ ] Password reset flow
- [ ] Profile editing
- [ ] Admin dashboard
- [ ] API key generation for businesses
- [ ] OAuth integration
- [ ] Multi-factor authentication
- [ ] Session management UI
- [ ] Audit log for auth events
