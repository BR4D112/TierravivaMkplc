package com.example.tierravivamarketplace.network

import com.example.tierravivamarketplace.io.response.PublishProduct
import retrofit2.http.GET

interface PublishProductService {
    @GET("mis_publicaciones")
    suspend fun getMyPubs(): List<PublishProduct>
}