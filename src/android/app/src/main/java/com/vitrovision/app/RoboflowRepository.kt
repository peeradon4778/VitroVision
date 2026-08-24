package com.vitrovision.app

import android.graphics.Bitmap
import android.util.Base64
import com.vitrovision.app.models.Prediction
import com.vitrovision.app.models.RoboflowRequest
import com.vitrovision.app.models.RoboflowResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.ByteArrayOutputStream
import java.util.concurrent.TimeUnit

class RoboflowRepository {

    private val api: RoboflowApi
    private val apiKey: String
    private val endpoint: String

    init {
        val logging = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        val client = OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .addInterceptor(logging)
            .build()

        val retrofit = Retrofit.Builder()
            .baseUrl("https://detect.roboflow.com/")
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        api = retrofit.create(RoboflowApi::class.java)
        apiKey = BuildConfig.ROBOFLOW_API_KEY
        endpoint = "${BuildConfig.ROBOFLOW_WORKSPACE}/${BuildConfig.ROBOFLOW_PROJECT}/${BuildConfig.ROBOFLOW_VERSION}"
    }

    suspend fun getPredictions(originalBitmap: Bitmap, prompts: List<String>): Result<RoboflowResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val (sendBitmap, scaleX, scaleY) = prepareBitmap(originalBitmap)

                val stream = ByteArrayOutputStream()
                sendBitmap.compress(Bitmap.CompressFormat.JPEG, 85, stream)
                val base64Image = Base64.encodeToString(stream.toByteArray(), Base64.NO_WRAP)

                val request = RoboflowRequest(image = base64Image, prompts = prompts)
                val response = api.segment(endpoint, apiKey, request)

                if (response.isSuccessful && response.body() != null) {
                    val roboflowResponse = response.body()!!
                    roboflowResponse.predictions?.let { preds ->
                        for (pred in preds) {
                            pred.points?.let { pts ->
                                val scaled = mutableListOf<List<Double>>()
                                for (pt in pts) {
                                    if (pt.size >= 2) {
                                        scaled.add(listOf(pt[0] * scaleX, pt[1] * scaleY))
                                    }
                                }
                                pred.points = scaled
                            }
                        }
                    }
                    Result.success(roboflowResponse)
                } else {
                    val errorMsg = response.errorBody()?.string() ?: "Unknown error"
                    Result.failure(Exception("API error ${response.code()}: $errorMsg"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }

    private fun prepareBitmap(original: Bitmap): Triple<Bitmap, Double, Double> {
        val origW = original.width.toDouble()
        val origH = original.height.toDouble()
        val maxDimension = 1280.0
        val maxSide = maxOf(origW, origH)
        if (maxSide <= maxDimension) {
            return Triple(original, 1.0, 1.0)
        }
        val ratio = maxDimension / maxSide
        val newW = (origW * ratio).toInt()
        val newH = (origH * ratio).toInt()
        val resized = Bitmap.createScaledBitmap(original, newW, newH, true)
        return Triple(resized, origW / newW, origH / newH)
    }
}
