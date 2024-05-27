package com.example.tierravivamarketplace.ui.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.PublishProduct

class MyPubsAdapter : ListAdapter<PublishProduct, MyPubsAdapter.MyPubsViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyPubsViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_pub, parent, false)
        return MyPubsViewHolder(view)
    }

    override fun onBindViewHolder(holder: MyPubsViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class MyPubsViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val productName: TextView = itemView.findViewById(R.id.product_name)
        private val unitValue: TextView = itemView.findViewById(R.id.unit_value)

        fun bind(publishProduct: PublishProduct) {
            productName.text = publishProduct.product_name
            unitValue.text = publishProduct.unit_value.toString()
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<PublishProduct>() {
        override fun areItemsTheSame(oldItem: PublishProduct, newItem: PublishProduct): Boolean {
            return oldItem.id_publish_prod == newItem.id_publish_prod
        }

        override fun areContentsTheSame(oldItem: PublishProduct, newItem: PublishProduct): Boolean {
            return oldItem == newItem
        }
    }
}
