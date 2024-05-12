def test_complex_clash(self):
    class Target(models.Model):
        tgt_safe = models.CharField(max_length=10)
        clash = models.CharField(max_length=10)
        model = models.CharField(max_length=10)

        clash1_set = models.CharField(max_length=10)

    class Model(models.Model):
        src_safe = models.CharField(max_length=10)

        foreign_1 = models.ForeignKey(Target, models.CASCADE, related_name="id")
        foreign_2 = models.ForeignKey(
            Target, models.CASCADE, related_name="src_safe"
        )

        m2m_1 = models.ManyToManyField(Target, related_name="id")
        m2m_2 = models.ManyToManyField(Target, related_name="src_safe")

    self.assertEqual(
        Model.check(),
        [
            Error(
                "Reverse accessor 'Target.id' for "
                "'invalid_models_tests.Model.foreign_1' clashes with field "
                "name 'invalid_models_tests.Target.id'.",
                hint=(
                    "Rename field 'invalid_models_tests.Target.id', or "
                    "add/change a related_name argument to the definition for "
                    "field 'invalid_models_tests.Model.foreign_1'."
                ),
                obj=Model._meta.get_field("foreign_1"),
                id="fields.E302",
            ),
            Error(
                "Reverse query name for 'invalid_models_tests.Model.foreign_1' "
                "clashes with field name 'invalid_models_tests.Target.id'.",
                hint=(
                    "Rename field 'invalid_models_tests.Target.id', or "
                    "add/change a related_name argument to the definition for "
                    "field 'invalid_models_tests.Model.foreign_1'."
                ),
                obj=Model._meta.get_field("foreign_1"),
                id="fields.E303",
            ),
            Error(
                "Reverse accessor 'Target.id' for "
                "'invalid_models_tests.Model.foreign_1' clashes with reverse "
                "accessor for 'invalid_models_tests.Model.m2m_1'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.foreign_1' or "
                    "'invalid_models_tests.Model.m2m_1'."
                ),
                obj=Model._meta.get_field("foreign_1"),
                id="fields.E304",
            ),
            Error(
                "Reverse query name for 'invalid_models_tests.Model.foreign_1' "
                "clashes with reverse query name for "
                "'invalid_models_tests.Model.m2m_1'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.foreign_1' or "
                    "'invalid_models_tests.Model.m2m_1'."
                ),
                obj=Model._meta.get_field("foreign_1"),
                id="fields.E305",
            ),
            Error(
                "Reverse accessor 'Target.src_safe' for "
                "'invalid_models_tests.Model.foreign_2' clashes with reverse "
                "accessor for 'invalid_models_tests.Model.m2m_2'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.foreign_2' or "
                    "'invalid_models_tests.Model.m2m_2'."
                ),
                obj=Model._meta.get_field("foreign_2"),
                id="fields.E304",
            ),
            Error(
                "Reverse query name for 'invalid_models_tests.Model.foreign_2' "
                "clashes with reverse query name for "
                "'invalid_models_tests.Model.m2m_2'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.foreign_2' or "
                    "'invalid_models_tests.Model.m2m_2'."
                ),
                obj=Model._meta.get_field("foreign_2"),
                id="fields.E305",
            ),
            Error(
                "Reverse accessor 'Target.id' for "
                "'invalid_models_tests.Model.m2m_1' clashes with field name "
                "'invalid_models_tests.Target.id'.",
                hint=(
                    "Rename field 'invalid_models_tests.Target.id', or "
                    "add/change a related_name argument to the definition for "
                    "field 'invalid_models_tests.Model.m2m_1'."
                ),
                obj=Model._meta.get_field("m2m_1"),
                id="fields.E302",
            ),
            Error(
                "Reverse query name for 'invalid_models_tests.Model.m2m_1' "
                "clashes with field name 'invalid_models_tests.Target.id'.",
                hint=(
                    "Rename field 'invalid_models_tests.Target.id', or "
                    "add/change a related_name argument to the definition for "
                    "field 'invalid_models_tests.Model.m2m_1'."
                ),
                obj=Model._meta.get_field("m2m_1"),
                id="fields.E303",
            ),
            Error(
                "Reverse accessor 'Target.id' for "
                "'invalid_models_tests.Model.m2m_1' clashes with reverse "
                "accessor for 'invalid_models_tests.Model.foreign_1'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.m2m_1' or "
                    "'invalid_models_tests.Model.foreign_1'."
                ),
                obj=Model._meta.get_field("m2m_1"),
                id="fields.E304",
            ),
            Error(
                "Reverse query name for 'invalid_models_tests.Model.m2m_1' "
                "clashes with reverse query name for "
                "'invalid_models_tests.Model.foreign_1'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.m2m_1' or "
                    "'invalid_models_tests.Model.foreign_1'."
                ),
                obj=Model._meta.get_field("m2m_1"),
                id="fields.E305",
            ),
            Error(
                "Reverse accessor 'Target.src_safe' for "
                "'invalid_models_tests.Model.m2m_2' clashes with reverse "
                "accessor for 'invalid_models_tests.Model.foreign_2'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.m2m_2' or "
                    "'invalid_models_tests.Model.foreign_2'."
                ),
                obj=Model._meta.get_field("m2m_2"),
                id="fields.E304",
            ),
            Error(
                "Reverse query name for 'invalid_models_tests.Model.m2m_2' "
                "clashes with reverse query name for "
                "'invalid_models_tests.Model.foreign_2'.",
                hint=(
                    "Add or change a related_name argument to the definition "
                    "for 'invalid_models_tests.Model.m2m_2' or "
                    "'invalid_models_tests.Model.foreign_2'."
                ),
                obj=Model._meta.get_field("m2m_2"),
                id="fields.E305",
            ),
        ],
    )