package com.example.tierravivamarketplace.ui

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.ui.adapters.MyPubsAdapter
class MyPubsActivity : AppCompatActivity() {

    private val viewModel: MyPubsViewModel by viewModels { MyPubsViewModelFactory(this) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_my_pubs)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val recyclerView: RecyclerView = findViewById(R.id.recycler_view)
        recyclerView.layoutManager = LinearLayoutManager(this)
        val adapter = MyPubsAdapter()
        recyclerView.adapter = adapter

        viewModel.myPubs.observe(this, Observer { publications ->
            adapter.submitList(publications)
        })

        viewModel.fetchMyPubs()
    }
}