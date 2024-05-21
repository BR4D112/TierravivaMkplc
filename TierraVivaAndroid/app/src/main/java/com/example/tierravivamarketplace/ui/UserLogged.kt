package com.example.tierravivamarketplace.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.Spinner
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.ActionBarDrawerToggle
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.GravityCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.drawerlayout.widget.DrawerLayout
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.Product
import com.example.tierravivamarketplace.network.ProductService
import com.example.tierravivamarketplace.network.RetrofitInstance
import com.google.android.material.navigation.NavigationView
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class UserLogged : AppCompatActivity() {

    private lateinit var productService: ProductService
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: ProductAdapter
    private var products = mutableListOf<Product>()
    private lateinit var drawerLayout: DrawerLayout
    private var select_categorie = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_user_logged)

        productService = RetrofitInstance.getProductService(this)
        //
        recyclerView = findViewById(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        adapter = ProductAdapter(products)
        recyclerView.adapter = adapter

        val spinnerCat = findViewById<Spinner>(R.id.spinner_categories_mainMenu)
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
                fetchProductsByCategory(selectedNumber)
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {
                // No action needed
            }
        }

        drawerLayout = findViewById(R.id.main)
        val navView: NavigationView = findViewById(R.id.nav_view)

        val toggle = ActionBarDrawerToggle(
            this, drawerLayout, null, R.string.navigation_drawer_open, R.string.navigation_drawer_close
        )
        drawerLayout.addDrawerListener(toggle)
        toggle.syncState()

        findViewById<ImageView>(R.id.imageLatBar).setOnClickListener {
            drawerLayout.openDrawer(GravityCompat.START)
        }

        navView.setNavigationItemSelectedListener { menuItem ->
            // Cerrar el drawer después de hacer clic en una opción del menú
            drawerLayout.closeDrawer(GravityCompat.START)

            // Manejar la acción según la opción seleccionada
            when (menuItem.itemId) {
                R.id.nav_item_profile -> {
                    // Ir a la actividad de perfil
                    startActivity(Intent(this, ProfileActivity::class.java))
                    true
                }

                R.id.nav_item_main_menu -> {
                    startActivity(Intent(this, UserLogged::class.java))
                    true
                }

                R.id.nav_item_add_prod -> {
                    startActivity(Intent(this, AddProdActivity::class.java))
                    true
                }

                R.id.nav_item_about_us -> {
                    startActivity(Intent(this, AboutUsActivity::class.java))
                    true
                }
                else -> false
            }
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun fetchProductsByCategory(idCategorie: Int) {
        productService.getProductsByCategorie(idCategorie).enqueue(object : Callback<List<Product>> {
            override fun onResponse(call: Call<List<Product>>, response: Response<List<Product>>) {
                if (response.isSuccessful) {
                    products.clear()
                    response.body()?.let { products.addAll(it) }
                    adapter.notifyDataSetChanged()
                }
            }

            override fun onFailure(call: Call<List<Product>>, t: Throwable) {
                // Manejar errores
            }
        })
    }

    override fun onBackPressed() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Confirmación")
        builder.setMessage("¿Estás seguro de que quieres cerrar sesión?")
        builder.setPositiveButton("Aceptar") { _, _ ->
            super.onBackPressed() // Cierra la aplicación o navega a la pantalla de inicio de sesión
        }
        builder.setNegativeButton("Cancelar") { dialog, _ ->
            dialog.dismiss() // Descarta el diálogo y mantiene al usuario en la actividad actual
        }
        builder.show()
    }
}
