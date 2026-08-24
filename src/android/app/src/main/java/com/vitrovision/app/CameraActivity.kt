package com.vitrovision.app

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.vitrovision.app.databinding.ActivityCameraBinding
import com.vitrovision.app.models.Prediction
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class CameraActivity : AppCompatActivity() {

    private lateinit var binding: ActivityCameraBinding
    private var imageCapture: ImageCapture? = null
    private lateinit var cameraExecutor: ExecutorService

    private val gson = Gson()
    private val repository = RoboflowRepository()
    private val daysSinceSubculture: Int get() = intent.getIntExtra("days_since_subculture", 0)

    private val resultLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == RESULT_OK) {
            setResult(RESULT_OK, result.data)
            finish()
        } else {
            binding.captureButton.isEnabled = true
        }
    }

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            startCamera()
        } else {
            Toast.makeText(this, "ต้องอนุญาตเข้าถึงกล้องก่อนใช้งาน", Toast.LENGTH_LONG).show()
            finish()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCameraBinding.inflate(layoutInflater)
        setContentView(binding.root)

        cameraExecutor = Executors.newSingleThreadExecutor()

        if (allPermissionsGranted()) {
            startCamera()
        } else {
            permissionLauncher.launch(Manifest.permission.CAMERA)
        }

        binding.captureButton.setOnClickListener {
            takePhoto()
        }

        binding.closeButton.setOnClickListener {
            finish()
        }
    }

    private fun allPermissionsGranted() = ContextCompat.checkSelfPermission(
        this, Manifest.permission.CAMERA
    ) == PackageManager.PERMISSION_GRANTED

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            val preview = Preview.Builder().build()
            preview.setSurfaceProvider(binding.previewView.surfaceProvider)

            imageCapture = ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build()

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    this,
                    androidx.camera.core.CameraSelector.DEFAULT_BACK_CAMERA,
                    preview,
                    imageCapture
                )
            } catch (e: Exception) {
                Toast.makeText(this, "เกิดข้อผิดพลาดในการเปิดกล้อง", Toast.LENGTH_SHORT).show()
                finish()
            }
        }, ContextCompat.getMainExecutor(this))
    }

    private fun takePhoto() {
        val imageCapture = imageCapture ?: return

        val photoFile = File(
            externalMediaDirs.firstOrNull()?.let {
                File(it, "captured_images").apply { mkdirs() }
            } ?: cacheDir,
            "vitro_${SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(System.currentTimeMillis())}.jpg"
        )

        val outputOptions = ImageCapture.OutputFileOptions.Builder(photoFile).build()

        imageCapture.takePicture(
            outputOptions,
            ContextCompat.getMainExecutor(this),
            object : ImageCapture.OnImageSavedCallback {
                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    val uri = Uri.fromFile(photoFile)
                    showConfirmDialog(uri)
                }

                override fun onError(exception: ImageCaptureException) {
                    Toast.makeText(this@CameraActivity, "บันทึกภาพล้มเหลว", Toast.LENGTH_SHORT).show()
                }
            }
        )
    }

    private fun showConfirmDialog(uri: Uri) {
        MaterialAlertDialogBuilder(this)
            .setTitle("ยืนยันภาพนี้")
            .setMessage("ต้องการใช้ภาพนี้ในการวิเคราะห์หรือไม่?")
            .setPositiveButton("ใช้ภาพนี้") { _, _ ->
                processImage(uri)
            }
            .setNegativeButton("ถ่ายใหม่") { _, _ -> }
            .show()
    }

    private fun processImage(uri: Uri) {
        binding.captureButton.isEnabled = false
        Toast.makeText(this, "กำลังประมวลผล…", Toast.LENGTH_SHORT).show()

        CoroutineScope(Dispatchers.Main).launch {
            val bitmap = withContext(Dispatchers.IO) {
                try {
                    val inputStream = contentResolver.openInputStream(uri)
                    BitmapFactory.decodeStream(inputStream)
                } catch (e: Exception) {
                    null
                }
            }

            if (bitmap == null) {
                Toast.makeText(this@CameraActivity, "ไม่สามารถอ่านภาพได้", Toast.LENGTH_SHORT).show()
                binding.captureButton.isEnabled = true
                return@launch
            }

            val result = withContext(Dispatchers.IO) {
                repository.getPredictions(bitmap, listOf("plant", "leaf"))
            }

            result.fold(
                onSuccess = { response ->
                    val predictionsJson = gson.toJson(response.predictions ?: emptyList())
                    val intent = Intent(this@CameraActivity, ResultActivity::class.java).apply {
                        putExtra("image_uri", uri.toString())
                        putExtra("predictions_json", predictionsJson)
                        putExtra("days_since_subculture", daysSinceSubculture)
                    }
                    resultLauncher.launch(intent)
                },
                onFailure = { error ->
                    Toast.makeText(this@CameraActivity, "เชื่อมต่อไม่ได้ กรุณาลองอีกครั้ง", Toast.LENGTH_LONG).show()
                    binding.captureButton.isEnabled = true
                }
            )
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
    }
}
