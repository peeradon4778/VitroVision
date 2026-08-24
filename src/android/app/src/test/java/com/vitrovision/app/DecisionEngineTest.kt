package com.vitrovision.app

import com.vitrovision.app.models.DecisionClass
import com.vitrovision.app.models.FeatureMetrics
import org.junit.Assert.assertEquals
import org.junit.Test

// ทดสอบขอบเขตการตัดสินใจของ DecisionEngine เทียบกับ research/subculture_criteria.md
// (days 21/45/60, coverage_ratio 0.35/0.70/0.80) ตามที่ audit_report.md section 3/6 ระบุว่ายังไม่มี test
class DecisionEngineTest {

    private fun metrics(
        coverage: Float,
        days: Int,
        shootCount: Int = 0,
        shootBaseline: Int? = null,
        glare: Float = 0f
    ) = FeatureMetrics(
        coverage_ratio = coverage,
        height_proxy = 0f,
        leaf_count = 0,
        shoot_count = shootCount,
        glare_score = glare,
        days_since_subculture = days,
        shoot_count_baseline = shootBaseline
    )

    // --- ขอบเขต days = 21 ---

    @Test
    fun `days ต่ำกว่า 21 ต้องเป็น WAIT เสมอไม่ว่า coverage เท่าไหร่`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.5f, days = 20))
        assertEquals(DecisionClass.WAIT, result.decision)
    }

    @Test
    fun `days เท่ากับ 21 พอดี กับ coverage ในช่วง ต้องเป็น SUBCULTURE`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.5f, days = 21))
        assertEquals(DecisionClass.SUBCULTURE, result.decision)
    }

    // --- ขอบเขต days = 45 ---

    @Test
    fun `days เท่ากับ 45 พอดี กับ coverage ในช่วง ต้องยังเป็น SUBCULTURE`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.5f, days = 45))
        assertEquals(DecisionClass.SUBCULTURE, result.decision)
    }

    @Test
    fun `days 46 เกินช่วง subculture และไม่มี baseline ตกไป WAIT`() {
        // หมายเหตุ: นี่คือ gap อีกจุดที่ยังไม่ resolve (คล้าย gap zone ของ coverage 0_70-0_80)
        // แต่ audit_report.md ระบุเฉพาะ gap ของ coverage — จุดนี้แค่ document ไว้ ไม่ได้แก้ในรอบนี้
        val result = DecisionEngine.decide(metrics(coverage = 0.5f, days = 46))
        assertEquals(DecisionClass.WAIT, result.decision)
    }

    // --- ขอบเขต days = 60 ---

    @Test
    fun `days เท่ากับ 60 พอดี ไม่ถูกนับเป็น TRANSPLANT_OVERDUE จาก days อย่างเดียว`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.5f, days = 60))
        assertEquals(DecisionClass.WAIT, result.decision)
    }

    @Test
    fun `days เกิน 60 ต้องเป็น TRANSPLANT_OVERDUE`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.1f, days = 61))
        assertEquals(DecisionClass.TRANSPLANT_OVERDUE, result.decision)
    }

    // --- ขอบเขต coverage_ratio = 0.35 ---

    @Test
    fun `coverage ต่ำกว่า 0_35 เล็กน้อย ต้องเป็น WAIT`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.34f, days = 30))
        assertEquals(DecisionClass.WAIT, result.decision)
    }

    @Test
    fun `coverage เท่ากับ 0_35 พอดี ต้องเป็น SUBCULTURE`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.35f, days = 30))
        assertEquals(DecisionClass.SUBCULTURE, result.decision)
    }

    // --- coverage_ratio = 0.70 (เดิมเป็นขอบบนของ SUBCULTURE ก่อน fix gap zone) ---

    @Test
    fun `coverage 0_70 อยู่ในช่วง SUBCULTURE`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.70f, days = 30))
        assertEquals(DecisionClass.SUBCULTURE, result.decision)
    }

    @Test
    fun `coverage 0_75 คือ gap zone เดิมที่เคยตกไป WAIT ตอนนี้ต้องเป็น SUBCULTURE หลัง fix`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.75f, days = 30))
        assertEquals(DecisionClass.SUBCULTURE, result.decision)
    }

    // --- ขอบเขต coverage_ratio = 0.80 ---

    @Test
    fun `coverage เท่ากับ 0_80 พอดี ยังเป็น SUBCULTURE ขอบรวมอยู่ในช่วงนี้`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.80f, days = 30))
        assertEquals(DecisionClass.SUBCULTURE, result.decision)
    }

    @Test
    fun `coverage เกิน 0_80 ต้องเป็น TRANSPLANT_OVERDUE`() {
        val result = DecisionEngine.decide(metrics(coverage = 0.81f, days = 30))
        assertEquals(DecisionClass.TRANSPLANT_OVERDUE, result.decision)
    }

    // --- shoot_count เทียบ baseline (relative growth rule) ---

    @Test
    fun `shoot_count นิ่งเทียบ baseline หลัง 45 วัน ต้องเป็น TRANSPLANT_OVERDUE`() {
        val result = DecisionEngine.decide(
            metrics(coverage = 0.5f, days = 50, shootCount = 11, shootBaseline = 10)
        )
        assertEquals(DecisionClass.TRANSPLANT_OVERDUE, result.decision)
    }

    @Test
    fun `shoot_count โตเกิน 1_2 เท่าของ baseline ไม่เข้าเงื่อนไข overdue จาก baseline`() {
        val result = DecisionEngine.decide(
            metrics(coverage = 0.5f, days = 50, shootCount = 13, shootBaseline = 10)
        )
        // ไม่เข้า TRANSPLANT_OVERDUE จาก baseline และไม่เข้า SUBCULTURE เพราะ days=50 อยู่นอกช่วง 21..45
        assertEquals(DecisionClass.WAIT, result.decision)
    }

    // --- glare_score ต้องลด confidence เท่านั้น ห้ามมีผลต่อ class ---

    @Test
    fun `glare_score สูงลด confidence แต่ต้องไม่เปลี่ยน decision class`() {
        val noGlare = DecisionEngine.decide(metrics(coverage = 0.5f, days = 30, glare = 0f))
        val withGlare = DecisionEngine.decide(metrics(coverage = 0.5f, days = 30, glare = 0.4f))

        assertEquals(noGlare.decision, withGlare.decision)
        assertEquals(noGlare.confidence * (1f - 0.4f * 0.5f), withGlare.confidence, 0.001f)
    }
}
