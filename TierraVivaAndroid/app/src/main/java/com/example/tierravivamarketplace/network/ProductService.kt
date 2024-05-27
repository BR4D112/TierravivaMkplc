package com.example.tierravivamarketplace.network

import com.example.tierravivamarketplace.io.response.Product
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path

interface ProductService {

    @GET("/product/{product_id}")
    fun getProductById(@Path("product_id") productId: Int): Call<Product>

    @GET("/categorie/{categoria_id}")
    fun getProductsByCategorie(@Path("categoria_id") categoriaId: Int): Call<List<Product>>

}