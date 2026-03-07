# Landowner Approval Workflow

## Overview
This workflow ensures landowners review and approve their land scan results before carbon credits are listed on the marketplace.

## Flow

### 1. **Land Registration** (Landowner)
- Landowner submits registration request via `/request-registration` page
- **Must include:**
  - Owner name and email
  - Land location (text description)
  - Land size and type
  - **Coordinates** (latitude, longitude of center point)
  - **Boundaries** (array of [lat, lon] points forming polygon)
  - Additional info (optional)
- Request stored with `status: 'pending'`
- Admin receives email notification

### 2. **Admin Scans Land**
- Admin views registration requests at `/admin/requests`
- Admin navigates to scan page with coordinates pre-filled
- Scan analyzes satellite imagery and generates:
  - Biomass estimate (tonnes/ha)
  - Carbon stock (tCO2e)
  - NDVI and EVI indices
  - Integrity score (0-100)
  - Risk assessment (0-100%)
  - Price valuation

### 3. **Credit Created with Pending Status**
After scan completes:
- Carbon credit created with `status: 'pending_approval'`
- **NOT listed on marketplace yet**
- Notification sent to landowner with scan findings:
  - Total carbon (tCO2e)
  - Price per tonne
  - Total value
  - Integrity score
  - Risk percentage
  - Biomass, NDVI, EVI data

### 4. **Landowner Reviews Results**
Landowner dashboard shows:
- Pending scans awaiting review
- All scan metrics (as shown in screenshot)
- Total valuation
- Risk assessment

Landowner can:
- ✅ **Accept** → Credit status changes to `listed` → Appears on marketplace
- ❌ **Reject** → Credit status changes to `rejected` → Hidden from marketplace

### 5. **Marketplace Listing** (After Approval)
Once approved:
- Credit status changes to `listed`
- Listed on marketplace at `/marketplace`
- Buyers can purchase
- Landowner receives payment

## API Endpoints

### For Landowners
```
POST   /api/registration/request          # Submit land registration with coordinates
GET    /api/landowner/pending-scans       # View scans awaiting approval
POST   /api/landowner/approve-listing     # Approve/reject credit listing
GET    /api/landowner/my-credits          # View all owned credits
GET    /api/notifications/me              # Get notifications
PATCH  /api/notifications/{id}/mark-read  # Mark notification as read
```

### For Admin
```
GET    /api/registration/requests         # View all registration requests
POST   /api/scan                          # Scan land and create pending credit
```

### Public
```
GET    /api/credits?status=listed         # Only shows approved credits
```

## Database Tables

### notifications
Stores landowner notifications:
```sql
- id (UUID)
- user_id (UUID) → references users
- type ('scan_complete', 'credit_approved', 'credit_sold', 'system')
- title (TEXT)
- message (TEXT)
- data (JSONB) → scan results, credit info
- read (BOOLEAN)
- created_at (TIMESTAMPTZ)
```

### carbon_credits
New status values:
- `pending_approval` → Awaiting landowner review
- `approved` → Landowner accepted (same as listed)
- `listed` → On marketplace (after approval)
- `sold` → Purchased by buyer
- `retired` → Used for offsetting
- `rejected` → Landowner declined

### registration_requests
Updated fields:
- `coordinates` (JSONB) → {lat, lon}
- `boundaries` (JSONB) → [[lat1, lon1], [lat2, lon2], ...]
- `scan_id` (UUID) → Link to scan result
- `credit_id` (UUID) → Link to carbon credit

## Frontend Components Needed

### 1. Update Registration Form
File: `frontend/src/app/request-registration/page.tsx`
- Add map component to select boundaries
- Add coordinate picker
- Store coordinates in form state

### 2. Create Landowner Dashboard
File: `frontend/src/app/landowner/dashboard.tsx` (new)
- Show pending scans
- Display scan results (like screenshot)
- "Accept" and "Reject" buttons
- Notifications panel

### 3. Update Navbar
- Add "My Land" or "Dashboard" link for landowners
- Show notification badge with unread count

## Migration

Run this SQL in Supabase:
```bash
# In Supabase SQL Editor, run:
backend/data/migration_approval_workflow.sql
```

This adds:
- `notifications` table
- Updated `carbon_credits` status constraint
- New columns to `registration_requests`

## Benefits

✅ **Landowner Control**: Owners decide whether to list their land
✅ **Transparency**: Owners see full scan details before listing
✅ **Trust**: No surprise listings without consent
✅ **Flexibility**: Owners can reject if unhappy with valuation
✅ **Audit Trail**: All approvals/rejections tracked

## Example Notification Data
```json
{
  "user_id": "uuid-of-landowner",
  "type": "scan_complete",
  "title": "Land Scan Complete - Review Results",
  "message": "Your land scan has been completed. Review the findings: 508.8 tCO2e valued at $2.00/tonne (Total: $1017.54). Please review and approve to list on marketplace.",
  "data": {
    "scan_id": "uuid",
    "credit_id": "uuid",
    "tco2e": 508.8,
    "price_per_tonne": 2.00,
    "total_value": 1017.54,
    "integrity_score": 55,
    "risk_score": 26,
    "biomass": 29.5,
    "ndvi": 0.446,
    "evi": 1.097
  },
  "read": false
}
```
