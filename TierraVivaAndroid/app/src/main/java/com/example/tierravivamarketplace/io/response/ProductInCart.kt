package com.example.tierravivamarketplace.io.response

data class ProductInCart(
    val id_publish_prod: Int,
    val product_name: String,
    val quantity: Int,
    val product_image: String, // Asumiendo que tienes URL de imagen en tu API
    val product_owner: String, // Asumiendo que tienes el propietario del producto en tu API
    val price: Double // Asumiendo que tienes el precio del producto en tu API
)
