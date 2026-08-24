package com.vitrovision.app

import com.vitrovision.app.models.DecisionClass
import com.vitrovision.app.models.FeatureMetrics
import com.vitrovision.app.models.TriageResult

object DecisionEngine {

    fun decide(metrics: FeatureMetrics): TriageResult {
        val days = metrics.days_since_subculture
        val coverage = metrics.coverage_ratio
        val shootCount = metrics.shoot_count.toFloat()
        val shootBaseline = metrics.shoot_count_baseline

        var decision: DecisionClass
        var baseConfidence = 0.85f

        when {
            days < 21 -> {
                decision = DecisionClass.WAIT
                baseConfidence = 0.90f
            }
            coverage > 0.80f || days > 60 -> {
                decision = DecisionClass.TRANSPLANT_OVERDUE
                baseConfidence = 0.88f
            }
            shootBaseline != null && days > 45 && shootCount < shootBaseline * 1.2f -> {
                decision = DecisionClass.TRANSPLANT_OVERDUE
                baseConfidence = 0.80f
            }
            // coverage_ratio ช่วง 0.70-0.80 เดิมไม่มีเงื่อนไขไหนครอบคลุม (ตกไป else -> WAIT)
            // ตัดสินใจ: รวมช่วงนี้เข้ากับ SUBCULTURE แทน เพราะ subculture_criteria.md ข้อ 1.3 ชี้ว่า
            // coverage ที่เพิ่มขึ้นเข้าใกล้ overcrowding (>0.80) คือสัญญาณ "ถึงเวลาย้าย" ไม่ใช่ "ให้รอ" —
            // การให้ WAIT ในช่วงนี้จะย้อนแย้งกับเหตุผลทางชีวภาพและเสี่ยงปล่อยให้ต้นไม้เข้าสู่ภาวะ
            // overcrowding/hyperhydricity โดยไม่แจ้งเตือนผู้ใช้ (ยังเป็น rough threshold รอ lab validate
            // เหมือนค่าขอบเขตอื่นทั้งหมดในไฟล์นี้ — ดู audit_report.md section 3 "Gap zone")
            coverage in 0.35f..0.80f && days in 21..45 -> {
                decision = DecisionClass.SUBCULTURE
                baseConfidence = 0.85f
            }
            else -> {
                decision = DecisionClass.WAIT
                baseConfidence = 0.75f
            }
        }

        val glarePenalty = metrics.glare_score * 0.5f
        val confidence = baseConfidence * (1f - glarePenalty).coerceIn(0f, 1f)

        return TriageResult(
            decision = decision,
            confidence = confidence
        )
    }
}
