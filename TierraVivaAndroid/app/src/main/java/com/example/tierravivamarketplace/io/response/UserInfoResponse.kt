package com.example.tierravivamarketplace.io.response

data class UserInfoResponse(
    val email: String,
    val first_name: String,
    val last_name: String,
    val doc_type: String,
    val doc_number: String,
    val phone_number: String,
    val location: String
)