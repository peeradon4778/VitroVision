package com.vitrovision.app.models

import com.google.gson.annotations.SerializedName

data class RoboflowRequest(
    @SerializedName("image") val image: String,
    @SerializedName("text_prompts") val prompts: List<String>
)
