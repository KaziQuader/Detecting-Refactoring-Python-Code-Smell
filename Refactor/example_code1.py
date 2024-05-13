def _resolve_weighted_web_vital_score_function(
    self,
    args: Mapping[str, Union[str, Column, SelectType, int, float]],
    alias: str,
    ) -> SelectType:
    column = args["column"]
    metric_id = args["metric_id"]
    if column not in [
        "measurements.score.lcp",
        "measurements.score.fcp",
        "measurements.score.fid",
        "measurements.score.cls",
        "measurements.score.ttfb",
    ]: 
        raise InvalidSearchQuery("performance_score only supports measurements")
    return Function(
        "greatest",
        [
            Function(
                "least",
                [
                    Function(
                        "if",
                        [
                            Function(
                                "and",
                                [
                                    Function(
                                        "greater",
                                        [
                                            Function(
                                                "sumIf",
                                                [
                                                    Column("value"),
                                                    Function(
                                                        "equals",
                                                        [Column("metric_id"), metric_id],
                                                    ),
                                                ],
                                            ),
                                            0,
                                        ],
                                    ),
                                    Function(
                                        "greater",
                                        [
                                            Function(
                                                "countIf",
                                                [
                                                    Column("value"),
                                                    Function(
                                                        "equals",
                                                        [
                                                            Column("metric_id"),
                                                            self.resolve_metric(
                                                                "measurements.score.total"
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            0,
                                        ],
                                    ),
                                ],
                            ),
                            Function(
                                "divide",
                                [
                                    Function(
                                        "sumIf",
                                        [
                                            Column("value"),
                                            Function(
                                                "equals", [Column("metric_id"), metric_id]
                                            ),
                                        ],
                                    ),
                                    Function(
                                        "countIf",
                                        [
                                            Column("value"),
                                            Function(
                                                "equals",
                                                [
                                                    Column("metric_id"),
                                                    self.resolve_metric(
                                                        "measurements.score.total"
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            0.0,
                        ],
                    ),
                    1.0,
                ],
            ),
            0.0,
        ],
        alias,
    )