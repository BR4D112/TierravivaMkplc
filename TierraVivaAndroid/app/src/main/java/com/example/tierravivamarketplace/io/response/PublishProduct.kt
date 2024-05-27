package com.example.tierravivamarketplace.io.response

data class PublishProduct(
    val id_publish_prod: Int,
    val id_product: Int,
    val id_user: Int,
    val product_name: String,
    val unit_value: Float,
    val quantity: Float,
    val description: String,
    val location: String,
    val image: String
)
