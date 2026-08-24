package com.vitrovision.app

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.vitrovision.app.databinding.ActivityResultBinding
import com.vitrovision.app.models.DecisionClass
import com.vitrovision.app.models.FeatureMetrics
import com.vitrovision.app.models.Prediction
import com.vitrovision.app.models.TriageResult
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ResultActivity : AppCompatActivity() {

    private lateinit var binding: ActivityResultBinding
    private val gson = Gson()

    private var originalBitmap: Bitmap? = null
    private var predictions: List<Prediction> = emptyList()
    private var metrics: FeatureMetrics? = null
    private var triageResult: TriageResult? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityResultBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val imageUriString = intent.getStringExtra("image_uri") ?: ""
        val predictionsJson = intent.getStringExtra("predictions_json") ?: "[]"
        val daysSinceSubculture = intent.getIntExtra("days_since_subculture", 0)

        val type = object : TypeToken<List<Prediction>>() {}.type
        predictions = gson.fromJson(predictionsJson, type)

        loadAndProcess(imageUriString, daysSinceSubculture)

        setupOverrideButtons()
        // ปิดปุ่ม override ไว้ก่อนจนกว่า loadAndProcess() จะจบ (กัน race ที่ triageResult ยังเป็น null
        // ถ้าผู้ใช้กดปุ่มระหว่างกำลังประมวลผล) — เปิดกลับใน displayResult()/displayNoPredictionsError()
        setOverrideButtonsEnabled(false)
        binding.backHomeButton.setOnClickListener {
            val resultIntent = intent.apply {
                // ถ้ายังไม่มี triageResult (เช่น ไม่พบต้นพืชในภาพและผู้ใช้ยังไม่ override เอง)
                // ต้องไม่ส่ง decision_class กลับไป — ห้าม fallback เป็น WAIT เพราะจะกลายเป็นสัญญาณ
                // false negative ซ้ำที่หน้าแรกเหมือนกับบั๊กที่ audit_report.md ระบุไว้
                triageResult?.let {
                    putExtra("decision_class", it.decision.name)
                    putExtra("confidence", it.confidence)
                }
            }
            setResult(RESULT_OK, resultIntent)
            finish()
        }
    }

    private fun loadAndProcess(imageUriString: String, daysSinceSubculture: Int) {
        CoroutineScope(Dispatchers.Main).launch {
            val bitmap = withContext(Dispatchers.IO) {
                try {
                    val uri = android.net.Uri.parse(imageUriString)
                    val inputStream = contentResolver.openInputStream(uri)
                    BitmapFactory.decodeStream(inputStream)
                } catch (e: Exception) {
                    null
                }
            }

            if (bitmap == null) {
                Toast.makeText(this@ResultActivity, "ไม่สามารถโหลดภาพได้", Toast.LENGTH_SHORT).show()
                return@launch
            }

            originalBitmap = bitmap

            val feats = FeatureExtractor.extract(bitmap, predictions, daysSinceSubculture)
            metrics = feats

            // SAM3 ไม่เจอ prediction เลย (ภาพว่าง/มองไม่เห็นต้นพืช) — ต้องแสดง error state แทนการ
            // ปล่อยให้ DecisionEngine ตัดสินจาก feature ที่เป็น 0 ทั้งหมด ซึ่งเดิมจะตกไปเป็น WAIT
            // ด้วย confidence 0.75 ทั้งที่ระบบไม่ได้ "เห็น" อะไรเลย (false negative ตาม audit_report.md)
            if (predictions.isEmpty()) {
                withContext(Dispatchers.Main) {
                    displayNoPredictionsError(bitmap, feats)
                }
                return@launch
            }

            val decision = DecisionEngine.decide(feats)
            triageResult = decision

            withContext(Dispatchers.Main) {
                displayResult(bitmap, feats, decision)
            }
        }
    }

    private fun displayResult(bitmap: Bitmap, feats: FeatureMetrics, decision: TriageResult) {
        binding.maskOverlay.setData(bitmap, predictions)

        binding.coverageValue.text = String.format("%.0f%%", feats.coverage_ratio * 100)
        binding.heightValue.text = String.format("%.0f%%", feats.height_proxy * 100)
        binding.leafCountValue.text = feats.leaf_count.toString()
        binding.shootCountValue.text = feats.shoot_count.toString()
        binding.glareValue.text = String.format("%.1f%%", feats.glare_score * 100)
        binding.daysValue.text = "${feats.days_since_subculture} วัน"

        val confPct = (decision.confidence * 100).toInt()
        binding.confidenceText.text = "ความเชื่อมั่น $confPct%"

        val (decisionText, decisionColor) = when (decision.decision) {
            DecisionClass.WAIT -> Pair("รอ", Color.parseColor("#F9A825"))
            DecisionClass.SUBCULTURE -> Pair("ย้ายได้", Color.parseColor("#2E7D32"))
            DecisionClass.TRANSPLANT_OVERDUE -> Pair("ย้ายด่วน", Color.parseColor("#C62828"))
        }

        binding.decisionText.text = decisionText
        binding.decisionText.setTextColor(decisionColor)
        binding.decisionCard.setCardBackgroundColor(
            Color.argb(30, Color.red(decisionColor), Color.green(decisionColor), Color.blue(decisionColor))
        )

        setOverrideButtonsEnabled(true)
    }

    private fun displayNoPredictionsError(bitmap: Bitmap, feats: FeatureMetrics) {
        binding.maskOverlay.setData(bitmap, predictions)

        binding.coverageValue.text = String.format("%.0f%%", feats.coverage_ratio * 100)
        binding.heightValue.text = String.format("%.0f%%", feats.height_proxy * 100)
        binding.leafCountValue.text = feats.leaf_count.toString()
        binding.shootCountValue.text = feats.shoot_count.toString()
        binding.glareValue.text = String.format("%.1f%%", feats.glare_score * 100)
        binding.daysValue.text = "${feats.days_since_subculture} วัน"

        val errorColor = Color.parseColor("#C62828") // @color/error
        binding.confidenceText.text = ""
        binding.decisionText.text = getString(R.string.no_predictions)
        binding.decisionText.setTextColor(errorColor)
        binding.decisionCard.setCardBackgroundColor(
            Color.argb(30, Color.red(errorColor), Color.green(errorColor), Color.blue(errorColor))
        )

        // ไม่ตั้ง triageResult จากผลอัตโนมัติ (ไม่มีให้ตั้ง เพราะ SAM3 ไม่เจออะไร) — ผู้ใช้ต้องกด
        // override เองถ้าต้องการบันทึกผล ตามกฎ "manual override ต้องมีเสมอ"
        setOverrideButtonsEnabled(true)
    }

    private fun setOverrideButtonsEnabled(enabled: Boolean) {
        binding.overrideWaitButton.isEnabled = enabled
        binding.overrideSubcultureButton.isEnabled = enabled
        binding.overrideTransplantButton.isEnabled = enabled
    }

    private fun setupOverrideButtons() {
        binding.overrideWaitButton.setOnClickListener {
            confirmOverride(DecisionClass.WAIT)
        }
        binding.overrideSubcultureButton.setOnClickListener {
            confirmOverride(DecisionClass.SUBCULTURE)
        }
        binding.overrideTransplantButton.setOnClickListener {
            confirmOverride(DecisionClass.TRANSPLANT_OVERDUE)
        }
    }

    private fun confirmOverride(override: DecisionClass) {
        val label = when (override) {
            DecisionClass.WAIT -> "รอ"
            DecisionClass.SUBCULTURE -> "ย้าย"
            DecisionClass.TRANSPLANT_OVERDUE -> "ย้ายด่วน"
        }

        MaterialAlertDialogBuilder(this)
            .setTitle("เปลี่ยนผลเป็น \"$label\"")
            .setMessage("การเปลี่ยนผลนี้จะแทนที่ผลจากระบบ โปรดยืนยัน")
            .setPositiveButton("ยืนยัน") { _, _ ->
                val overrideResult = TriageResult(
                    decision = override,
                    confidence = triageResult?.confidence ?: 0f,
                    manualOverride = true
                )
                triageResult = overrideResult
                val color = when (override) {
                    DecisionClass.WAIT -> Color.parseColor("#F9A825")
                    DecisionClass.SUBCULTURE -> Color.parseColor("#2E7D32")
                    DecisionClass.TRANSPLANT_OVERDUE -> Color.parseColor("#C62828")
                }
                binding.decisionText.text = label
                binding.decisionText.setTextColor(color)
                binding.decisionCard.setCardBackgroundColor(
                    Color.argb(30, Color.red(color), Color.green(color), Color.blue(color))
                )
                Toast.makeText(this, "เปลี่ยนผลเรียบร้อย", Toast.LENGTH_SHORT).show()
            }
            .setNegativeButton("ยกเลิก", null)
            .show()
    }
}
