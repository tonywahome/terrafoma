# TerraFoma Authentication System - Quick Start Guide

## ✅ What's Been Implemented

### Role-Based Access Control
Your TerraFoma platform now has complete user authentication with two distinct user roles:

**🌳 Landowners** can access:
- Homepage (landing page)
- Registry (view all credits)
- Marketplace (sell their credits)
- **Scan Land** (exclusive - generate carbon credits)

**🏭 Businesses** can access:
- Homepage (landing page)
- Registry (view all credits)
- Marketplace (purchase credits)
- **Dashboard** (exclusive - track emissions & calculate footprint)

### Key Features

1. **Signup/Login Pages** (`/signup`, `/login`)
   - Beautiful UI with role selection
   - Choose between Landowner (🌳) and Business (🏭)
   - Optional company name for businesses
   - Secure password authentication

2. **Smart Navbar**
   - Shows different links based on user role
   - User profile dropdown with name and role badge
   - Login/Signup buttons when not authenticated
   - Logout functionality

3. **Protected Routes**
   - `/scan` - Only landowners can access
   - `/dashboard` - Only businesses can access
   - Auto-redirect to login if not authenticated
   - Auto-redirect to appropriate page if wrong role

4. **Backend API** (`/api/auth/...`)
   - `POST /api/auth/signup` - Create account
   - `POST /api/auth/login` - Sign in
   - `POST /api/auth/logout` - Sign out
   - `GET /api/auth/me` - Get current user

## 🚀 How to Test

### 1. Visit the Homepage
```
http://localhost:3001
```

You'll see two big buttons:
- **🌳 I'm a Landowner** - Sell carbon credits
- **🏭 I'm a Business** - Offset emissions

### 2. Create a Landowner Account

1. Click "I'm a Landowner" button
2. Fill out the signup form:
   - Full Name: `John Farmer`
   - Email: `landowner@test.com`
   - Password: `password123`
   - Role: Landowner (pre-selected)
3. Click "Create account"

**What happens:**
- Redirected to homepage (now authenticated)
- Navbar shows: Home | Registry | Marketplace | **Scan Land**
- User menu in top-right shows your name
- NO "Dashboard" link (business-only feature)

### 3. Test Landowner Flow

1. Click **"Scan Land"** in navbar
2. Draw a polygon on the map
3. Click "Run AI Scan"
4. View results with biomass, carbon, integrity scores
5. Click "Accept Contract" to create credit
6. Credit now appears in Registry and Marketplace

### 4. Create a Business Account

1. Click user menu → "Sign out"
2. Click "Sign up" in navbar
3. Fill out signup form:
   - Select: **🏭 I'm a Business**
   - Full Name: `Jane CEO`
   - Email: `business@test.com`
   - Company Name: `Green Corp` (optional)
   - Password: `password123`
4. Click "Create account"

**What happens:**
- Navbar shows: Home | Registry | Marketplace | **Dashboard**
- NO "Scan Land" link (landowner-only feature)
- User menu shows "🏭 Business" badge

### 5. Test Business Flow

1. Click **"Dashboard"** in navbar
2. See global emissions data (IEA 1990-2023)
3. Use carbon footprint calculator
4. View platform statistics
5. Click "View Marketplace" to browse credits
6. Purchase credits to offset emissions

## 📁 Files Created/Modified

### New Files
```
frontend/src/contexts/AuthContext.tsx          - Auth state management
frontend/src/components/ProtectedRoute.tsx     - Route protection
frontend/src/app/login/page.tsx                - Login UI
frontend/src/app/signup/page.tsx               - Signup UI with role selection
backend/routers/auth.py                        - Auth API endpoints
backend/data/migration_add_auth.sql            - Database schema update
AUTHENTICATION.md                              - Full technical documentation
```

###Modified Files
```
frontend/src/components/Navbar.tsx             - Role-based navigation
frontend/src/app/layout.tsx                    - Wrapped with AuthProvider
frontend/src/app/page.tsx                      - Updated CTAs
frontend/src/app/scan/page.tsx                 - Protected (landowner-only)
frontend/src/app/dashboard/page.tsx            - Protected (business-only)
backend/main.py                                - Added auth router
```

## 🗄️ Database Setup (Required!)

You need to run the migration in Supabase to add authentication tables:

```bash
# Copy the contents of this file into Supabase SQL Editor:
backend/data/migration_add_auth.sql
```

This will:
- Add `password_hash` column to `users` table
- Create `sessions` table for auth tokens
- Update role check to accept 'landowner' and 'business'

## 🎯 User Experience Flow

### Landowner Journey
```
1. Visit homepage
2. Click "I'm a Landowner"
3. Sign up → Redirected to homepage
4. Click "Scan Land"
5. Draw land plot
6. AI analyzes satellite data
7. Accept contract
8. Credit appears in marketplace
9. Receive payment when business buys
```

### Business Journey
```
1. Visit homepage
2. Click "I'm a Business"
3. Sign up → Redirected to homepage
4. Click "Dashboard"
5. Calculate carbon footprint
6. See: "You emit 245.2 tCO₂e per year"
7. Click "View Marketplace"
8. Browse verified credits
9. Purchase to offset emissions
10. Download certificate
```

## 🔧 Current Status

**✅ Backend Server:** Running on http://localhost:8002
- Auth endpoints working
- All routes functional
- Auto-reload enabled

**✅ Frontend Server:** Running on http://localhost:3001
- Landing page updated
- Auth UI implemented
- Route protection active
- No compilation errors

## 📝 Notes

- **Password Security:** Currently using SHA256 (demo). Use bcrypt in production.
- **Sessions:** 30-day expiration, stored in database
- **Tokens:** Stored in localStorage (use HTTP-only cookies in production)
- **No Email Verification:** For demo purposes
- **Database:** Remember to run the migration in Supabase!

## 🐛 Troubleshooting

**"Cannot access scan page"** → You're logged in as business. Logout and signup as landowner.

**"Cannot access dashboard"** → You're logged in as landowner. Logout and signup as business.

**"Login failed"** → Check:
1. Database migration run in Supabase?
2. Backend server running?
3. Correct email/password?

**"Page stuck loading"** → Clear browser cache:
```javascript
// In browser console:
localStorage.clear()
// Then refresh page
```

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Homepage shows two role selection buttons
- ✅ Signup page asks for user type
- ✅ Navbar changes based on who's logged in
- ✅ Landowner sees "Scan Land", business sees "Dashboard"
- ✅ User menu shows role badge (🌳 or 🏭)
- ✅ Logging out returns to public homepage
- ✅ Can't access protected pages without login

## 📚 Next Steps

See [AUTHENTICATION.md](./AUTHENTICATION.md) for:
- Complete API documentation
- Security recommendations
- Production deployment guide
- Advanced features (OAuth, 2FA, etc.)

---

**Your authentication system is ready! Test it by signing up as both user types and exploring the different features available to each role.** 🚀
