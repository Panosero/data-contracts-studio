# Data Directory

This directory contains local development database files and data storage.

## Files

- `*.db` - SQLite database files for local development
- `*.sqlite*` - SQLite database variants
- Database backups and snapshots

## Important Notes

⚠️ **Do not commit database files to version control**

- Database files contain sensitive data and can be large
- They are environment-specific and should not be shared
- Use database migrations (Alembic) to manage schema changes instead

## Database Initialization

For a fresh development setup:

1. **Create new database:**
   ```bash
   # From backend directory
   alembic upgrade head
   ```

2. **Reset database (if needed):**
   ```bash
   # Remove existing database
   rm data/*.db
   
   # Recreate with migrations
   alembic upgrade head
   ```

## Backup

To backup your local development data:

```bash
# Create backup
cp data/data_contracts.db data/backup_$(date +%Y%m%d_%H%M%S).db

# Or use SQLite dump
sqlite3 data/data_contracts.db .dump > data/backup_$(date +%Y%m%d_%H%M%S).sql
```

---

This directory is managed by the backend application and should not be manually modified unless you know what you're doing.
