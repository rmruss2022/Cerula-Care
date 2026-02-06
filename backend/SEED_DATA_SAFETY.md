# Seed Data Safety

## Overview

The seed script (`seed_data.py`) is designed to be **completely safe** and **idempotent**. This means:

✅ **Safe to run multiple times** - It will never delete existing data
✅ **Checks before inserting** - Only adds data that doesn't already exist
✅ **Never drops tables** - Only creates tables if they don't exist
✅ **No data loss** - Existing records are preserved

## How It Works

1. **Care Team Members**: Checks by email before inserting
2. **Patients**: Checks by email before inserting  
3. **Assignments**: Checks by patient_id + member_id before inserting
4. **Health Screenings**: Checks by patient_id + date before inserting

## Running the Seed Script

### Via API Endpoint (Recommended)
```bash
curl -X POST https://cerula-care-production.up.railway.app/api/admin/seed
```

This endpoint is safe to call multiple times. It will:
- Show current database state
- Only add missing data
- Return counts of all entities

### Via Railway CLI
```bash
cd backend
railway run python seed_data.py
```

## Preventing Data Loss

### What We've Done

1. **Idempotent Seed Functions**: All seed functions check for existing data
2. **No DROP Statements**: `Base.metadata.create_all()` only creates tables, never drops
3. **Transaction Safety**: Uses database transactions with rollback on errors
4. **Detailed Logging**: Shows what's being added vs what already exists

### Railway Database Persistence

Railway PostgreSQL databases are persistent by default. However, if you notice data disappearing:

1. **Check Railway Dashboard**: Verify the PostgreSQL service is running
2. **Check DATABASE_URL**: Ensure it's pointing to the correct database
3. **Verify No Manual Resets**: Check if anyone manually reset the database
4. **Check Logs**: Review Railway logs for any errors

### If Data Gets Deleted

If data disappears, simply run the seed script again:

```bash
curl -X POST https://cerula-care-production.up.railway.app/api/admin/seed
```

The script will restore all seed data without affecting any manually added data (as long as emails/keys don't conflict).

## Current Seed Data

- **7 Care Team Members**: Health Coaches, BHCMs, and Psychiatrists
- **10 Patients**: Various statuses (active, inactive, discharged)
- **17 Care Team Assignments**: Members assigned to patients
- **60 Health Screenings**: 6 months of data per patient

## Best Practices

1. **Don't modify seed_data.py** to delete data - it's designed to only add
2. **Use the API endpoint** for easy reseeding if needed
3. **Monitor Railway logs** if data disappears unexpectedly
4. **Backup important data** if you add custom records beyond seed data
