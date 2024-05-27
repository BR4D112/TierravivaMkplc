package com.example.tierravivamarketplace.network

import com.example.tierravivamarketplace.io.response.CartItems
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface CartService {

    interface CartService {
        @POST("crear_y_agregar_carrito")
        suspend fun crearYAgregarCarrito(@Body items: CartItems): Response<Map<String, Any>>
    }
}