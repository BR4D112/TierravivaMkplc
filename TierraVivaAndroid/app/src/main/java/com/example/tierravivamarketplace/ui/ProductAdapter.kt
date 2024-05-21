package com.example.tierravivamarketplace.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.Product
import android.widget.ImageView
import android.widget.TextView
import com.squareup.picasso.Picasso

class ProductAdapter(private val products: List<Product>) : RecyclerView.Adapter<ProductAdapter.ProductViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_product, parent, false)
        return ProductViewHolder(view)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        val product = products[position]
        holder.productName.text = product.product_name
        holder.productDescription.text = product.description
        holder.productPrice.text = "COP ${product.unit_value}"
        Picasso.get().load(product.image).into(holder.productImage)
    }

    override fun getItemCount(): Int = products.size

    class ProductViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val productName: TextView = view.findViewById(R.id.productName)
        val productDescription: TextView = view.findViewById(R.id.productDescription)
        val productPrice: TextView = view.findViewById(R.id.productPrice)
        val productImage: ImageView = view.findViewById(R.id.productImage)
    }
}