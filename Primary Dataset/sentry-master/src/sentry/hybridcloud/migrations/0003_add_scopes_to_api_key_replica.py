# Generated by Django 3.2.20 on 2023-09-27 09:06

from django.db import migrations

import bitfield.models
import sentry.db.models.fields.array
from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production. For
    # the most part, this should only be used for operations where it's safe to run the migration
    # after your code has deployed. So this should not be used for most operations that alter the
    # schema of a table.
    # Here are some things that make sense to mark as dangerous:
    # - Large data migrations. Typically we want these to be run manually by ops so that they can
    #   be monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   have ops run this and not block the deploy. Note that while adding an index is a schema
    #   change, it's completely safe to run the operation after the code has deployed.
    is_dangerous = False

    dependencies = [
        ("hybridcloud", "0002_add_slug_reservation_replica_model"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    """
                    ALTER TABLE "hybridcloud_apikeyreplica" ADD COLUMN "scopes" BIGINT NOT NULL DEFAULT 0;
                    ALTER TABLE "hybridcloud_apikeyreplica" ADD COLUMN "scope_list" TEXT NULL;
                    """,
                    reverse_sql="""
                    ALTER TABLE "hybridcloud_apikeyreplica" DROP COLUMN "scopes";
                    ALTER TABLE "hybridcloud_apikeyreplica" DROP COLUMN "scope_list";
                    """,
                    hints={"tables": ["hybridcloud_apikeyreplica"]},
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="apikeyreplica",
                    name="scope_list",
                    field=sentry.db.models.fields.array.ArrayField(null=True),
                ),
                migrations.AddField(
                    model_name="apikeyreplica",
                    name="scopes",
                    field=bitfield.models.BitField(
                        [
                            "project:read",
                            "project:write",
                            "project:admin",
                            "project:releases",
                            "team:read",
                            "team:write",
                            "team:admin",
                            "event:read",
                            "event:write",
                            "event:admin",
                            "org:read",
                            "org:write",
                            "org:admin",
                            "member:read",
                            "member:write",
                            "member:admin",
                        ],
                        default=None,
                    ),
                ),
            ],
        ),
    ]
