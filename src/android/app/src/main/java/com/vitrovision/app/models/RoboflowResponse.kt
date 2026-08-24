package com.vitrovision.app.models

import com.google.gson.annotations.SerializedName

data class RoboflowResponse(
    @SerializedName("predictions") val predictions: List<Prediction>?,
    @SerializedName("time") val time: Double?
)
