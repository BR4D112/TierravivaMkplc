package com.example.tierravivamarketplace.ui.adapters

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.tierravivamarketplace.R
import com.example.tierravivamarketplace.io.response.PublishProduct
import com.example.tierravivamarketplace.network.RetrofitInstance
import com.example.tierravivamarketplace.ui.MyPubsActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MyPubsAdapter(private val context: Context) : ListAdapter<PublishProduct, MyPubsAdapter.MyPubsViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyPubsViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_pub, parent, false)
        return MyPubsViewHolder(view, context)
    }

    override fun onBindViewHolder(holder: MyPubsViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class MyPubsViewHolder(itemView: View, private val context: Context) : RecyclerView.ViewHolder(itemView) {
        private val productName: TextView = itemView.findViewById(R.id.product_name)
        private val unitValue: TextView = itemView.findViewById(R.id.unit_value)
        private val deleteIcon: ImageView = itemView.findViewById(R.id.delete_pub_icn)

        fun bind(publishProduct: PublishProduct) {
            productName.text = publishProduct.product_name
            unitValue.text = publishProduct.unit_value.toString()

            deleteIcon.setOnClickListener {
                val productService = RetrofitInstance.getProductService(context)
                val call = productService.deleteProduct(publishProduct.id_publish_prod)

                call.enqueue(object : Callback<Void> {
                    override fun onResponse(call: Call<Void>, response: Response<Void>) {
                        if (response.isSuccessful) {
                            Toast.makeText(
                                context,
                                "Producto eliminado exitosamente",
                                Toast.LENGTH_SHORT
                            ).show()
                            (itemView.context as? MyPubsActivity)?.let { activity ->
                                activity.viewModel.fetchMyPubs()
                            }
                        } else {
                            Toast.makeText(
                                context,
                                "Error al eliminar el producto",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }

                    override fun onFailure(call: Call<Void>, t: Throwable) {
                        Toast.makeText(context, "Error de conexión", Toast.LENGTH_SHORT).show()
                    }
                })
            }
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
