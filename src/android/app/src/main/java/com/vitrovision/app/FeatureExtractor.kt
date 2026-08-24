package com.vitrovision.app

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import com.vitrovision.app.models.FeatureMetrics
import com.vitrovision.app.models.Prediction

/**
 * ตั้งค่า ROI (Region of Interest) — ตัวหารร่วมของ coverage_ratio, height_proxy, glare_score
 * ตามนิยามใน research/_orchestration.md
 *
 * สมมติฐานปัจจุบัน: ถ่ายภาพที่ระยะห่างจากขวดคงที่ (fixed-distance capture ตาม proposal
 * section 7.1.1 และ diagram pipeline) ทำให้ขวดเข้าเต็มเฟรมโดยประมาณ ⇒ ROI ≈ ทั้งภาพ
 * (marginRatio = 0f = ค่า default ปัจจุบัน)
 *
 * marginRatio > 0f = ตัดขอบภาพออกแบบ center-crop สมมาตรทุกด้าน (เผื่อพื้นหลัง/โต๊ะ/มือติดขอบเฟรม)
 * เป็นทางเลือกชั่วคราวก่อนมี bottle/ROI detector จริง (ยังไม่สร้างรอบนี้ตาม audit_report.md section 6
 * — หนักเกินและยังไม่ถึงเวลา) วาง config นี้ไว้เป็นจุดต่อ (extension point): เมื่อมี detector จริงในอนาคต
 * ให้แทนที่การคำนวณ roiLeft/roiTop/roiRight/roiBottom ใน extract() ด้วย bounding box ที่ detector
 * คืนมาแทน โดยไม่ต้องแก้ signature ของ extract()
 */
data class RoiConfig(
    val marginRatio: Float = 0f
)

object FeatureExtractor {

    private const val MIN_CONFIDENCE = 0.5

    fun extract(
        bitmap: Bitmap,
        predictions: List<Prediction>,
        daysSinceSubculture: Int,
        roiConfig: RoiConfig = RoiConfig()
    ): FeatureMetrics {
        val width = bitmap.width
        val height = bitmap.height

        // ROI rect ปัจจุบัน (ดูคอมเมนต์ที่ RoiConfig ด้านบน) — default marginRatio=0f ทำให้
        // roiLeft/roiTop=0 และ roiRight/roiBottom=width/height นั่นคือ ROI ≈ ทั้งภาพ
        val marginRatio = roiConfig.marginRatio.coerceIn(0f, 0.49f)
        val roiLeft = (width * marginRatio).toInt()
        val roiTop = (height * marginRatio).toInt()
        val roiRight = width - roiLeft
        val roiBottom = height - roiTop
        val roiWidth = roiRight - roiLeft
        val roiHeight = roiBottom - roiTop
        val roiPixelCount = roiWidth * roiHeight

        val maskBitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        val maskCanvas = Canvas(maskBitmap)
        val fillPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            style = Paint.Style.FILL
            color = Color.WHITE
        }

        var leafCount = 0
        var shootCount = 0
        var maxPlantHeight = 0.0
        var hasPlantBbox = false

        for (pred in predictions) {
            val className = pred.class_name ?: continue
            val confidence = pred.confidence ?: 0.0

            val pts = pred.points
            if (pts != null && pts.size >= 3) {
                val path = Path()
                var first = true
                for (pt in pts) {
                    if (pt.size >= 2) {
                        val px = pt[0].toFloat()
                        val py = pt[1].toFloat()
                        if (first) {
                            path.moveTo(px, py)
                            first = false
                        } else {
                            path.lineTo(px, py)
                        }
                    }
                }
                path.close()
                maskCanvas.drawPath(path, fillPaint)
            }

            if (className.equals("leaf", ignoreCase = true) && confidence >= MIN_CONFIDENCE) {
                leafCount++
            }

            // shoot_count เดิมนับทุก prediction โดยไม่มี confidence filter (ต่างจาก leaf_count ด้านบน)
            // ทำให้ prediction confidence ต่ำดันไปเฟ้อจำนวนยอด — ใส่ threshold เดียวกันให้ตรงกัน
            if ((className.equals("plant", ignoreCase = true) || className.equals("shoot", ignoreCase = true)) &&
                confidence >= MIN_CONFIDENCE
            ) {
                shootCount++
                val bboxH = pred.height ?: 0.0
                if (bboxH > maxPlantHeight) {
                    maxPlantHeight = bboxH
                    hasPlantBbox = true
                }
            }
        }

        val coveragePixels = countNonZeroPixelsInRoi(maskBitmap, roiLeft, roiTop, roiRight, roiBottom)
        val coverageRatio = if (roiPixelCount > 0) coveragePixels.toFloat() / roiPixelCount else 0f

        val heightProxy = if (hasPlantBbox && roiHeight > 0) {
            (maxPlantHeight / roiHeight).toFloat()
        } else 0f

        val glareScore = calculateGlareScore(bitmap, roiLeft, roiTop, roiRight, roiBottom)

        maskBitmap.recycle()

        return FeatureMetrics(
            coverage_ratio = coverageRatio,
            height_proxy = heightProxy,
            leaf_count = leafCount,
            shoot_count = shootCount,
            glare_score = glareScore,
            days_since_subculture = daysSinceSubculture
        )
    }

    private fun countNonZeroPixelsInRoi(bitmap: Bitmap, left: Int, top: Int, right: Int, bottom: Int): Int {
        val roiWidth = right - left
        if (roiWidth <= 0) return 0
        val rowPixels = IntArray(roiWidth)
        var count = 0
        for (y in top until bottom) {
            bitmap.getPixels(rowPixels, 0, roiWidth, left, y, roiWidth, 1)
            for (pixel in rowPixels) {
                if (pixel != Color.TRANSPARENT) {
                    count++
                }
            }
        }
        return count
    }

    fun calculateGlareScore(
        bitmap: Bitmap,
        roiLeft: Int = 0,
        roiTop: Int = 0,
        roiRight: Int = bitmap.width,
        roiBottom: Int = bitmap.height
    ): Float {
        val left = roiLeft.coerceIn(0, bitmap.width)
        val top = roiTop.coerceIn(0, bitmap.height)
        val right = roiRight.coerceIn(left, bitmap.width)
        val bottom = roiBottom.coerceIn(top, bitmap.height)
        val w = right - left
        val h = bottom - top
        if (w <= 0 || h <= 0) return 0f

        var glareCount = 0
        val total = w * h
        val rowPixels = IntArray(w)

        for (y in top until bottom) {
            bitmap.getPixels(rowPixels, 0, w, left, y, w, 1)
            for (pixel in rowPixels) {
                val r = Color.red(pixel)
                val g = Color.green(pixel)
                val b = Color.blue(pixel)

                val min = minOf(r, g, b)
                val max = maxOf(r, g, b)
                val diff = max - min

                val v = max / 255.0f
                val s = if (max == 0) 0f else diff.toFloat() / max

                if (v > 0.95f && s < 0.2f) {
                    glareCount++
                }
            }
        }

        return glareCount.toFloat() / total
    }
}
