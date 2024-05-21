package com.example.tierravivamarketplace.io.response

data class Product(
    val product_name: String,
    val unit_value: Float,
    val quantity: Float,
    val description: String,
    val location: String,
    val image: String
)
