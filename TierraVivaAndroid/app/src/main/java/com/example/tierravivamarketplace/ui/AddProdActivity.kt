package com.example.tierravivamarketplace.ui

import android.media.Image
import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Spinner
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia.*
import androidx.activity.result.registerForActivityResult
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.ProductCreateRequest
import com.example.tierravivamarketplace.network.RetrofitInstance
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class AddProdActivity : AppCompatActivity() {

    val pickMedia = registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        if (uri != null) {
            imgView.setImageURI(uri)
            println("uri ${uri}")
            selected_img = uri.toString()
        } else {
            //no img
        }
    }
    lateinit var btnImg: Button
    lateinit var imgView: ImageView
    private var select_categorie = 0
    private var select_measure = 0
    private var selected_img = ""


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_add_prod)
        btnImg = findViewById(R.id.sel_img_btn)
        imgView = findViewById(R.id.img_selected)
        btnImg.setOnClickListener {
            pickMedia.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
        }
        val btn: Button = findViewById(R.id.pub_prod_btn)
        btn.setOnClickListener {

            val inputProdName: EditText = findViewById(R.id.inputProdName)
            val value: EditText = findViewById(R.id.inputValProd)
            val inputQuantity: EditText = findViewById(R.id.inputQuantity)
            val locationSpinner: Spinner = findViewById(R.id.spinner_prod_locations)
            val descriptionIn: EditText = findViewById(R.id.inputDescription)
            val id_categorie = select_categorie
            val id_measure_prod = select_measure
            val product_name = inputProdName.text.toString()
            val unit_value = value.text.toString().toFloatOrNull() ?: 0f
            val quantity = inputQuantity.text.toString().toFloatOrNull() ?: 0f
            val description = descriptionIn.text.toString()
            val location = locationSpinner.selectedItem.toString()
            val image = selected_img

            println("categoria: ${id_categorie}")
            println("id_measure_prod: ${id_measure_prod}")
            println("nombre: ${product_name}")
            println("unitVal: ${unit_value}")
            println("cantidad: ${quantity}")
            println("descripcion: ${description}")
            println("ubicacion: ${location}")
            println("imagen: ${image}")
            val product = ProductCreateRequest(id_categorie, id_measure_prod, product_name, unit_value, quantity, description, location, image)
            createProduct(product)
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        val spinnerCat = findViewById<Spinner>(R.id.spinner_categories)
        val optionCat = arrayOf("Hortalizas", "Frutas", "Tuberculos")
        spinnerCat.adapter = ArrayAdapter<String>(applicationContext, android.R.layout.simple_spinner_item, optionCat)
        spinnerCat.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                val selectItem = parent?.getItemAtPosition(position).toString()
                val selectedNumber = when (selectItem) {
                    "Hortalizas" -> 1
                    "Frutas" -> 2
                    "Tuberculos" -> 3
                    else -> 0
                }
                select_categorie = selectedNumber
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {
                TODO("Not yet implemented")
            }
        }
        val spinnerMeas = findViewById<Spinner>(R.id.spinner_measures)
        val optionMeas = arrayOf("Canastas", "Arrobas", "Toneladas", "Bultos")
        spinnerMeas.adapter = ArrayAdapter<String>(applicationContext, android.R.layout.simple_spinner_item, optionMeas)
        spinnerMeas.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                val selectItem = parent?.getItemAtPosition(position).toString()
                val selectedNumber = when (selectItem) {
                    "Canastas" -> 1
                    "Arrobas" -> 2
                    "Toneladas" -> 3
                    "Bultos" -> 4
                    else -> 0
                }
                select_measure = selectedNumber
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {
                TODO("Not yet implemented")
            }
        }

        val spinnerLocations = findViewById<Spinner>(R.id.spinner_prod_locations)
        val optionLocations = resources.getStringArray(R.array.boy_muni)
        val adapter = ArrayAdapter(applicationContext,android.R.layout.simple_spinner_item, optionLocations)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerLocations.adapter = adapter
    }

    private fun createProduct(product: ProductCreateRequest) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val response = RetrofitInstance.getAuthService(this@AddProdActivity).createProduct(product)
                withContext(Dispatchers.Main) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@AddProdActivity, "Producto publicado exitosamente", Toast.LENGTH_SHORT).show()
                    } else {
                        Toast.makeText(this@AddProdActivity, "Error al publicar el producto", Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    Toast.makeText(this@AddProdActivity, "Error de red: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
}