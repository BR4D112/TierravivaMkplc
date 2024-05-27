package com.example.tierravivamarketplace.ui

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.UserInfoResponse
import com.example.tierravivamarketplace.network.RetrofitInstance
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ProfileActivity : AppCompatActivity() {

    private lateinit var firstNameTextView: TextView
    private lateinit var lastNameTextView: TextView
    private lateinit var docTypeTextView: TextView
    private lateinit var docNumberTextView: TextView
    private lateinit var phoneNumberTextView: TextView
    private lateinit var locationTextView: TextView
    private lateinit var emailTextView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_profile)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        firstNameTextView = findViewById(R.id.firstNameTextView)
        lastNameTextView = findViewById(R.id.lastNameTextView)
        docTypeTextView = findViewById(R.id.docTypeTextView)
        docNumberTextView = findViewById(R.id.docNumberTextView)
        phoneNumberTextView = findViewById(R.id.phoneNumberTextView)
        locationTextView = findViewById(R.id.locationTextView)
        emailTextView = findViewById(R.id.emailTextView)

        getUserInfo()
    }

    private fun getUserInfo() {
        val authService = RetrofitInstance.getAuthService(this)
        authService.getUserInfo().enqueue(object : Callback<UserInfoResponse> {
            override fun onResponse(call: Call<UserInfoResponse>, response: Response<UserInfoResponse>) {
                if (response.isSuccessful) {
                    val userInfo = response.body()
                    if (userInfo != null) {
                        firstNameTextView.text = userInfo.first_name
                        lastNameTextView.text = userInfo.last_name
                        docTypeTextView.text = userInfo.doc_type
                        docNumberTextView.text = userInfo.doc_number
                        phoneNumberTextView.text = userInfo.phone_number
                        locationTextView.text = userInfo.location
                        emailTextView.text = userInfo.email
                    }
                } else {
                    Toast.makeText(this@ProfileActivity, "Error al obtener la información del usuario", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<UserInfoResponse>, t: Throwable) {
                Toast.makeText(this@ProfileActivity, "Fallo en la solicitud: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }

}