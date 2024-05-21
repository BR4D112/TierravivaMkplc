package com.example.tierravivamarketplace.io.response

data class ProductCreateRequest(
    val id_categorie: Int,
    val id_measure_prod: Int,
    val product_name: String,
    val unit_value: Float,
    val quantity: Float,
    val description: String,
    val location: String,
    val image: String
)
