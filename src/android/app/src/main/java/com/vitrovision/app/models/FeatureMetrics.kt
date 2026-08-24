package com.vitrovision.app.models

data class FeatureMetrics(
    val coverage_ratio: Float,
    val height_proxy: Float,
    val leaf_count: Int,
    val shoot_count: Int,
    val glare_score: Float,
    val days_since_subculture: Int,
    val shoot_count_baseline: Int? = null
)
