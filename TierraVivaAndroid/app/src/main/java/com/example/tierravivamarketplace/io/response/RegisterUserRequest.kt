package com.example.tierravivamarketplace.io.response

data class RegisterUserRequest(
    val person: Person,
    val email: String,
    val credit_number: String,
    val password: String
)
