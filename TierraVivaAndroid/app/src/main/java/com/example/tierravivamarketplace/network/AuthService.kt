package com.example.tierravivamarketplace.network

import com.example.tierravivamarketplace.io.response.LoginCredentials
import com.example.tierravivamarketplace.io.response.LoginResponse
import com.example.tierravivamarketplace.io.response.ProductCreateRequest
import com.example.tierravivamarketplace.io.response.RegisterUserRequest
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthService {
    @POST("login")
    suspend fun login(@Body credentials: LoginCredentials): Response<LoginResponse>

    @POST("register")
    fun registerUser(@Body registerUserRequest: RegisterUserRequest): Call<ResponseBody>

    @POST("product_register")
    suspend fun createProduct(@Body product: ProductCreateRequest): Response<ResponseBody>

}