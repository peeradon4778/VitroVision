package com.vitrovision.app.models

enum class DecisionClass {
    WAIT,
    SUBCULTURE,
    TRANSPLANT_OVERDUE
}

data class TriageResult(
    val decision: DecisionClass,
    val confidence: Float,
    var manualOverride: Boolean = false
)
