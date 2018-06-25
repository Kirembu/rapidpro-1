# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-19 20:03
from __future__ import unicode_literals

from django.db import migrations

SQL = """
----------------------------------------------------------------------
-- Trigger procedure to update user and system labels on column changes
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_on_change() RETURNS TRIGGER AS $$
DECLARE
  _is_test BOOLEAN;
  _new_label_type CHAR(1);
  _old_label_type CHAR(1);
BEGIN
  IF TG_OP IN ('INSERT', 'UPDATE') THEN
    -- prevent illegal message states
    IF NEW.direction = 'I' AND NEW.status NOT IN ('P', 'H') THEN
      RAISE EXCEPTION 'Incoming messages can only be PENDING or HANDLED';
    END IF;
    IF NEW.direction = 'O' AND NEW.visibility = 'A' THEN
      RAISE EXCEPTION 'Outgoing messages cannot be archived';
    END IF;
  END IF;

  -- new message inserted
  IF TG_OP = 'INSERT' THEN
    -- don't update anything for a test message
    IF temba_contact_is_test(NEW.contact_id) THEN
      RETURN NULL;
    END IF;

    _new_label_type := temba_msg_determine_system_label(NEW);
    IF _new_label_type IS NOT NULL THEN
      PERFORM temba_insert_system_label(NEW.org_id, _new_label_type, FALSE, 1);
    END IF;

    IF NEW.broadcast_id IS NOT NULL THEN
      PERFORM temba_insert_broadcastmsgcount(NEW.broadcast_id, 1);
    END IF;

  -- existing message updated
  ELSIF TG_OP = 'UPDATE' THEN
    _old_label_type := temba_msg_determine_system_label(OLD);
    _new_label_type := temba_msg_determine_system_label(NEW);

    IF _old_label_type IS DISTINCT FROM _new_label_type THEN
      -- don't update anything for a test message
      IF temba_contact_is_test(NEW.contact_id) THEN
        RETURN NULL;
      END IF;

      IF _old_label_type IS NOT NULL THEN
        PERFORM temba_insert_system_label(OLD.org_id, _old_label_type, FALSE, -1);
      END IF;
      IF _new_label_type IS NOT NULL THEN
        PERFORM temba_insert_system_label(NEW.org_id, _new_label_type, FALSE, 1);
      END IF;
    END IF;

    -- is being archived or deleted (i.e. no longer included for user labels)
    IF OLD.visibility = 'V' AND NEW.visibility != 'V' THEN
      PERFORM temba_insert_message_label_counts(NEW.id, FALSE, -1);
    END IF;

    -- is being restored (i.e. now included for user labels)
    IF OLD.visibility != 'V' AND NEW.visibility = 'V' THEN
      PERFORM temba_insert_message_label_counts(NEW.id, FALSE, 1);
    END IF;

    -- update our broadcast msg count if it changed
    IF NEW.broadcast_id IS DISTINCT FROM OLD.broadcast_id THEN
      PERFORM temba_insert_broadcastmsgcount(OLD.broadcast_id, -1);
      PERFORM temba_insert_broadcastmsgcount(NEW.broadcast_id, 1);
    END IF;

  -- existing message deleted
  ELSIF TG_OP = 'DELETE' THEN
    -- don't update anything for a test message
    IF temba_contact_is_test(OLD.contact_id) THEN
      RETURN NULL;
    END IF;

    _old_label_type := temba_msg_determine_system_label(OLD);

    IF _old_label_type IS NOT NULL THEN
      IF OLD.delete_reason = 'A' THEN
        PERFORM temba_insert_system_label(OLD.org_id, _old_label_type, FALSE, -1);
        PERFORM temba_insert_system_label(OLD.org_id, _old_label_type, TRUE, 1);
      ELSE
        PERFORM temba_insert_system_label(OLD.org_id, _old_label_type, FALSE, -1);
      END IF;

    END IF;

    IF OLD.broadcast_id IS NOT NULL AND OLD.delete_reason != 'A' THEN
      PERFORM temba_insert_broadcastmsgcount(OLD.broadcast_id, -1);
    END IF;

  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS temba_msg_on_change_trg ON msgs_msg;
CREATE TRIGGER temba_msg_on_change_trg
  AFTER INSERT OR UPDATE OR DELETE ON msgs_msg
  FOR EACH ROW EXECUTE PROCEDURE temba_msg_on_change();

----------------------------------------------------------------------
-- Inserts a new channelcount row with the given values
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_insert_broadcastmsgcount(_broadcast_id INTEGER, _count INT) RETURNS VOID AS $$
  BEGIN
    IF _broadcast_id IS NOT NULL THEN
      INSERT INTO msgs_broadcastmsgcount("broadcast_id", "count", "is_squashed")
        VALUES(_broadcast_id, _count, FALSE);
    END IF;
  END;
$$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [("msgs", "0123_broadcastmsgcount")]

    operations = [migrations.RunSQL(SQL, "")]