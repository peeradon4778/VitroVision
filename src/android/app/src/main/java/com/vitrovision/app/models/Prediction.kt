package com.vitrovision.app.models

import com.google.gson.annotations.SerializedName

data class Prediction(
    @SerializedName("class") val class_name: String?,
    @SerializedName("confidence") val confidence: Double?,
    @SerializedName("x") val x: Double?,
    @SerializedName("y") val y: Double?,
    @SerializedName("width") val width: Double?,
    @SerializedName("height") val height: Double?,
    @SerializedName("points") val points: List<List<Double>>?,
    @SerializedName("mask") val mask: Any?
)
