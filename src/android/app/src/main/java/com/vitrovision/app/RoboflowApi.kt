package com.vitrovision.app

import com.vitrovision.app.models.RoboflowRequest
import com.vitrovision.app.models.RoboflowResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface RoboflowApi {

    @POST("{endpoint}")
    suspend fun segment(
        @Path("endpoint", encoded = true) endpoint: String,
        @Query("api_key") apiKey: String,
        @Body request: RoboflowRequest
    ): Response<RoboflowResponse>
}
