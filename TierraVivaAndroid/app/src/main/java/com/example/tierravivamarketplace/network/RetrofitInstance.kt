package com.example.tierravivamarketplace.network

import android.content.Context
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


object RetrofitInstance {
    private const val BASE_URL = "http://192.168.42.214:8000/"

    private fun getClient(context: Context): OkHttpClient {
        return OkHttpClient.Builder().apply {
            addInterceptor { chain ->
                val request = chain.request().newBuilder()
                    .addHeader("Authorization", "Bearer ${YourTokenStorage.getToken(context)}")
                    .build()
                chain.proceed(request)
            }
        }.build()
    }

    private fun getRetrofit(context: Context): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .client(getClient(context))
            .build()
    }

    fun getAuthService(context: Context): AuthService {
        return getRetrofit(context).create(AuthService::class.java)
    }

    fun getProductService(context: Context): ProductService {
        return getRetrofit(context).create(ProductService::class.java)
    }

    fun getCartService(context: Context): CartService {
        return getRetrofit(context).create(CartService::class.java)
    }

    fun getPublishProductService(context: Context): PublishProductService {
        return getRetrofit(context).create(PublishProductService::class.java)
    }

}