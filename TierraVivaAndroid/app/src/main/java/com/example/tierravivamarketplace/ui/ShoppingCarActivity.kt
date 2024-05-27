package com.example.tierravivamarketplace.ui

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.ProductInCart
import com.example.tierravivamarketplace.network.CarService
import com.example.tierravivamarketplace.network.RetrofitInstance
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ShoppingCarActivity : AppCompatActivity() {

    private lateinit var cartService: CarService
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: CartProductAdapter
    private var products = mutableListOf<ProductInCart>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_shopping_car)

        //cartService = RetrofitInstance.getCartService(this)

        recyclerView = findViewById(R.id.recyclerShopView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        adapter = CartProductAdapter(products)
        recyclerView.adapter = adapter

        fetchProductsInCart()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun fetchProductsInCart() {
        CoroutineScope(Dispatchers.Main).launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    cartService.getCarritoDeCompras()
                }

                if (response.isSuccessful) {
                    products.clear()
                    response.body()?.let { products.addAll(it) }
                    adapter.notifyDataSetChanged()
                } else {
                    // Manejar error de solicitud
                }
            } catch (e: Exception) {
                // Manejar excepción
            }
        }
    }
}