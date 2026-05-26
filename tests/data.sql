INSERT INTO user (username, password)
VALUES
  ('admin', 'scrypt:32768:8:1$9F5i8ciYcx1AFVLe$564e6357db07ae14685a74f824d74e91b46a7d47568f97c11b1b0ee395d4a7eb3b2d235b1a566393ae5f4482bdb2eb476916aa33a230fcccc600faf474f4f7e8'),
  ('other', 'scrypt:32768:8:1$EL2bGG8pCVsp32p8$4c2b2b7150b0bd0551cc12c7ea941621abdd26fd2a5c67c5f867e1521d8e0a1b423209ed37d7c00894ae5b575937424402b2177abb493bb8d866e1844be4137e');

INSERT INTO entry_type (name, unit)
VALUES
  ('Food', 'g');
  ('Dog walk',)

INSERT INTO log_entry (author_id, event_time, family_member_id, entry_type_id, amount, comments)
VALUES
  (1, '2026-01-01 12:00:00', NULL, 1, 200, 'Lunch'),
  (1, '2026-01-01 18:00:00', NULL, 1, 100, 'Dinner'),
  (2, '2026-01-02 08:00:00', NULL, 2, NULL, 'Morning walk');