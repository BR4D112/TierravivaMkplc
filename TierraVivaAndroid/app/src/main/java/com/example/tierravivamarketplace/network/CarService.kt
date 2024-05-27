package com.example.tierravivamarketplace.network

import com.example.tierravivamarketplace.io.response.ProductInCart
import retrofit2.Response
import retrofit2.http.GET

interface CarService {
    @GET("carrito_de_compras")
    suspend fun getCarritoDeCompras(): Response<List<ProductInCart>>
}