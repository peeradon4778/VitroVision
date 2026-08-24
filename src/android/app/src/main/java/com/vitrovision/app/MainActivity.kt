package com.vitrovision.app

import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.vitrovision.app.databinding.ActivityMainBinding
import com.vitrovision.app.models.DecisionClass

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    private val cameraLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == RESULT_OK) {
            val decisionClass = result.data?.getStringExtra("decision_class")
            val confidence = result.data?.getFloatExtra("confidence", 0f)
            if (decisionClass != null) {
                updateLastResult(decisionClass, confidence ?: 0f)
            }
        }
    }

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            launchCamera()
        } else {
            Toast.makeText(this, "ต้องอนุญาตเข้าถึงกล้องก่อนใช้งาน", Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.captureButton.setOnClickListener {
            val days = parseDays()
            if (days < 0) {
                MaterialAlertDialogBuilder(this)
                    .setTitle("ยืนยัน")
                    .setMessage("กรุณากรอกจำนวนวันหลังย้ายครั้งล่าสุด")
                    .setPositiveButton("ตกลง", null)
                    .show()
            } else {
                checkPermission(days)
            }
        }
    }

    private fun parseDays(): Int {
        val text = binding.daysInput.text.toString()
        val days = text.toIntOrNull()
        return days ?: -1
    }

    private fun checkPermission(days: Int) {
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.CAMERA) ==
            PackageManager.PERMISSION_GRANTED) {
            launchCamera()
        } else {
            permissionLauncher.launch(android.Manifest.permission.CAMERA)
        }
    }

    private fun launchCamera() {
        val days = parseDays()
        val intent = Intent(this, CameraActivity::class.java)
        intent.putExtra("days_since_subculture", maxOf(days, 0))
        cameraLauncher.launch(intent)
    }

    private fun updateLastResult(decisionClass: String, confidence: Float) {
        binding.lastResultText.visibility = android.view.View.GONE
        binding.lastResultDetail.visibility = android.view.View.VISIBLE

        val classText = try {
            when (DecisionClass.valueOf(decisionClass)) {
                DecisionClass.WAIT -> "รอ"
                DecisionClass.SUBCULTURE -> "ย้ายได้"
                DecisionClass.TRANSPLANT_OVERDUE -> "ย้ายด่วน"
            }
        } catch (e: IllegalArgumentException) {
            "ไม่ทราบ"
        }
        val confPct = (confidence * 100).toInt()
        binding.lastResultDetail.text = "$classText (ความเชื่อมั่น $confPct%)"
    }
}
