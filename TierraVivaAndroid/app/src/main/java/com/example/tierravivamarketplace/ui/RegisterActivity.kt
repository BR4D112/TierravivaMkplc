package com.example.tierravivamarketplace.ui

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.Person
import com.example.tierravivamarketplace.io.response.RegisterUserRequest
import com.example.tierravivamarketplace.network.AuthService
import com.example.tierravivamarketplace.network.RetrofitInstance
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class RegisterActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_register)

        val btn: Button = findViewById(R.id.next_btn)
        btn.setOnClickListener {
            btn.isEnabled = false

            val inputName: EditText = findViewById(R.id.inputName)
            val inputLastName: EditText = findViewById(R.id.inputLastName)
            val spinnerdocs: Spinner = findViewById(R.id.spinner_docs)
            val inputNoDoc: EditText = findViewById(R.id.inputNoDoc)
            val inputPhoneNum: EditText = findViewById(R.id.inputPhoneNum)
            val spinnerlocations: Spinner = findViewById(R.id.spinner_locations)
            val inputEmail: EditText = findViewById(R.id.inputEmail)
            val inputCreditNum: EditText = findViewById(R.id.inputCreditNum)
            val inputPassword: EditText = findViewById(R.id.inputPassword)
            val first_name = inputName.text.toString()
            val last_name = inputLastName.text.toString()
            val doc_type = spinnerdocs.selectedItem.toString()
            val doc_number = inputNoDoc.text.toString()
            val phone_number = inputPhoneNum.text.toString()
            val location = spinnerlocations.selectedItem.toString()
            val email = inputEmail.text.toString()
            val credit_number = inputCreditNum.text.toString()
            val password = inputPassword.text.toString()

            println("inputName: ${inputName.text}")
            println("inputLastName: ${inputLastName.text}")
            println("spinnerdocs: ${spinnerdocs.selectedItem}")
            println("inputPhoneNum: ${inputPhoneNum.text}")
            println("inputNoDoc: ${inputNoDoc.text}")
            println("spinnerlocations: ${spinnerlocations.selectedItem}")
            println("inputEmail: ${inputEmail.text}")
            println("inputCreditNum: ${inputCreditNum.text}")
            println("inputPassword: ${inputPassword.text}")
            println("firstName: $first_name")
            println("lastName: $last_name")
            println("docType: $doc_type")
            println("docNumber: $doc_number")
            println("phoneNumber: $phone_number")
            println("location: $location")
            println("email: $email")
            println("creditNumber: $credit_number")
            println("password: $password")

            val person = Person(first_name, last_name, doc_type, doc_number, phone_number, location)
            println("person: $person")
            val registerUserRequest = RegisterUserRequest(person, email, credit_number, password)
            println("register: $registerUserRequest")

            registerUser(registerUserRequest)
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val spinnerDoc = findViewById<Spinner>(R.id.spinner_docs)
        val optionDoc = arrayOf("C. Ciudadanía", "C. Extranjería")
        spinnerDoc.adapter = ArrayAdapter<String>(applicationContext, android.R.layout.simple_spinner_item, optionDoc)

        val spinnerLocations = findViewById<Spinner>(R.id.spinner_locations)
        val optionLocations = resources.getStringArray(R.array.boy_muni)
        val adapter = ArrayAdapter(applicationContext,android.R.layout.simple_spinner_item, optionLocations)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerLocations.adapter = adapter
    }

    private fun registerUser(registerUserRequest: RegisterUserRequest) {
        val authService = RetrofitInstance.getAuthService(this)
        authService.registerUser(registerUserRequest)
            .enqueue(object : Callback<ResponseBody> {
                override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                    if (response.isSuccessful) {
                        // Manejo de la respuesta exitosa
                        Log.d("Sendind JSON","correcto")
                        val intent = Intent(this@RegisterActivity, RegisterActivityII::class.java)
                        startActivity(intent)
                    } else {
                        // Manejo de errores
                        Log.d("Sendind JSON","error proceso")
                    }
                }

                override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                    // Manejo de errores
                    Log.d("Sendind JSON","error")
                }
            })
    }
}