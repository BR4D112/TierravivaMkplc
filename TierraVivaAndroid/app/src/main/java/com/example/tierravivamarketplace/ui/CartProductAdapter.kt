package com.example.tierravivamarketplace.ui

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.ProductInCart
import com.bumptech.glide.Glide

class CartProductAdapter(private val products: List<ProductInCart>) : RecyclerView.Adapter<CartProductAdapter.ViewHolder>() {

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val productImage: ImageView = itemView.findViewById(R.id.productImage)
        val productName: TextView = itemView.findViewById(R.id.productName)
        val productOwner: TextView = itemView.findViewById(R.id.productOwner)
        val productPrice: TextView = itemView.findViewById(R.id.productPrice)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.shopping_prod, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val product = products[position]
        holder.productName.text = product.product_name
        holder.productOwner.text = product.product_owner
        holder.productPrice.text = "${product.price} COP"

        // Cargar imagen con una librería como Glide o Picasso
        Glide.with(holder.itemView.context)
            .load(product.product_image)
            .into(holder.productImage)
    }

    override fun getItemCount() = products.size
}
