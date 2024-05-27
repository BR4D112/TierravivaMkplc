package com.example.tierravivamarketplace.ui

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.Product
import com.example.tierravivamarketplace.network.ProductService
import com.example.tierravivamarketplace.network.RetrofitInstance
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import com.squareup.picasso.Picasso
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ProductDetailActivity : AppCompatActivity() {

    private lateinit var productService: ProductService
    private lateinit var productImage: ImageView
    private lateinit var productName: TextView
    private lateinit var productDescription: TextView
    private lateinit var productPrice: TextView
    private lateinit var productLocation: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_product_detail)

        productService = RetrofitInstance.getProductService(this)

        productImage = findViewById(R.id.productImageGet)
        productName = findViewById(R.id.productNameGet)
        productDescription = findViewById(R.id.productDescriptionGet)
        productPrice = findViewById(R.id.productPriceGet)
        productLocation = findViewById(R.id.productLocationGet)

        val productId = intent.getIntExtra("PRODUCT_ID", -1)

        println("id producto: $productId")
        Log.d("ProductDetailActivity", "Received productId: $productId")

        if (productId != -1) {
            fetchProductDetails(productId)
        } else {
            Log.e("ProductDetailActivity", "Invalid productId received")
            // Handle the error appropriately
        }
    }

    private fun fetchProductDetails(productId: Int) {
        productService.getProductById(productId).enqueue(object : Callback<Product> {
            @SuppressLint("SetTextI18n")
            override fun onResponse(call: Call<Product>, response: Response<Product>) {
                if (response.isSuccessful) {
                    response.body()?.let { product ->
                        productName.text = product.product_name
                        productDescription.text = product.description
                        productPrice.text = "Precio: ${product.unit_value}"
                        productLocation.text = "Ubicación: ${product.location}"
                        Picasso.get().load(product.image).into(productImage)
                    }
                }
            }

            override fun onFailure(call: Call<Product>, t: Throwable) {
                // Manejar errores
            }
        })
    }
}