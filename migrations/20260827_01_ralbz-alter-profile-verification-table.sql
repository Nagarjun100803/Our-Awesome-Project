-- alter profile-verification table
-- depends: 20260825_01_uwahv-alter-user-table-adding-lastlogin-serial-key-for-user-id-purpose

-- migrate: apply
ALTER TABLE profile_verification ADD COLUMN verified_by UUID DEFAULT NULL REFERENCES users(id);

-- migrate: rollback
ALTER TABLE profile_verification DROP COLUMN verified_by;
