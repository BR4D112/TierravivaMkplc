package com.example.tierravivamarketplace.ui

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.tierravivamarketplace.R

class AddProdActivityII : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_add_prod_ii)

        val btn_back: Button = findViewById(R.id.back_to_menu)
        btn_back.setOnClickListener {
            val intent: Intent = Intent(this, UserLogged::class.java)
            startActivity(intent)
        }

        val btn_showMyPubs: Button = findViewById(R.id.show_my_pubs)
        btn_showMyPubs.setOnClickListener {
            val intent = Intent(this, MyPubsActivity::class.java)
            startActivity(intent)
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }
}