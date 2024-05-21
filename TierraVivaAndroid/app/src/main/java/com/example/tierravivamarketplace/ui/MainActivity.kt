package com.example.tierravivamarketplace.ui

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.LoginCredentials
import com.example.tierravivamarketplace.io.response.LoginResponse
import com.example.tierravivamarketplace.network.RetrofitInstance
import com.example.tierravivamarketplace.network.YourTokenStorage
import kotlinx.coroutines.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        val btnReg: Button = findViewById(R.id.registerbutton)
        btnReg.setOnClickListener {
            val intent: Intent = Intent(this, RegisterActivity::class.java)
            startActivity(intent)
        }

        val btnLogin: Button = findViewById(R.id.enterbutton)
        btnLogin.setOnClickListener {
            val emailEditText: EditText = findViewById(R.id.editTextEmailText)
            val passwordEditText: EditText = findViewById(R.id.editTextTextPassword)
            val email = emailEditText.text.toString()
            val password = passwordEditText.text.toString()
            login(email, password)
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun login(email: String, password: String) {
        CoroutineScope(Dispatchers.Main).launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    RetrofitInstance.getAuthService(this@MainActivity).login(LoginCredentials(email, password))
                }

                if (response.isSuccessful) {
                    val loginResponse = response.body()
                    val accessToken = loginResponse?.accessToken
                    YourTokenStorage.saveToken(accessToken, this@MainActivity)
                    // Manejar inicio de sesión exitoso
                    val intent = Intent(this@MainActivity, UserLogged::class.java)
                    startActivity(intent)
                } else {
                    // Manejar error de inicio de sesión
                    val errorCode = response.code()
                    if (errorCode == 400) {
                        // Credenciales incorrectas
                        showErrorMessage("Credenciales incorrectas")
                    } else {
                        // Otro error
                        showErrorMessage("Error de inicio de sesión: ${response.message()}")
                    }
                }
            } catch (e: Exception) {
                // Manejar cualquier excepción
                showErrorMessage("Error: ${e.message}")
                e.printStackTrace()
            }
        }
    }

    private fun showErrorMessage(message: String) {
        // Mostrar el mensaje de error en un Toast o una alerta de diálogo
        runOnUiThread {
            android.widget.Toast.makeText(this@MainActivity, message, android.widget.Toast.LENGTH_SHORT).show()
        }
    }

    override fun onBackPressed() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Confirmación")
        builder.setMessage("¿Estás seguro de que quieres salir de Tierra Viva?")
        builder.setPositiveButton("Aceptar") { _, _ ->
            super.onBackPressed() // Cierra la aplicación o navega a la pantalla de inicio de sesión
        }
        builder.setNegativeButton("Cancelar") { dialog, _ ->
            dialog.dismiss() // Descarta el diálogo y mantiene al usuario en la actividad actual
        }
        builder.show()
    }
}
