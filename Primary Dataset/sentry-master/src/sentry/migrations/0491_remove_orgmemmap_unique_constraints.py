# Generated by Django 2.2.28 on 2023-06-21 19:08

from django.db import migrations

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
        ("sentry", "0490_add_is_test_to_org"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE "sentry_organizationmembermapping" DROP CONSTRAINT "sentry_organizationmembe_organization_id_email_66a560fc_uniq";
            ALTER TABLE "sentry_organizationmembermapping" DROP CONSTRAINT "sentry_organizationmembe_organization_id_user_id_feb6bdf0_uniq";
            """,
            reverse_sql="",
            hints={"tables": ["sentry_organizationmembermapping"]},
        ),
        migrations.AlterIndexTogether(
            name="organizationmembermapping",
            index_together={("organization_id", "email"), ("organization_id", "user")},
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterUniqueTogether(
                    name="organizationmembermapping",
                    unique_together={("organization_id", "organizationmember_id")},
                ),
            ]
        ),
    ]
