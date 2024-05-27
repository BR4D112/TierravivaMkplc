package com.example.tierravivamarketplace.ui

import android.content.Context
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.tierravivamarketplace.io.response.PublishProduct
import com.example.tierravivamarketplace.network.RetrofitInstance
import kotlinx.coroutines.launch

class MyPubsViewModel(private val context: Context) : ViewModel() {

    private val _myPubs = MutableLiveData<List<PublishProduct>>()
    val myPubs: LiveData<List<PublishProduct>> get() = _myPubs

    fun fetchMyPubs() {
        viewModelScope.launch {
            try {
                val publications = RetrofitInstance.getPublishProductService(context).getMyPubs()
                _myPubs.postValue(publications)
            } catch (e: Exception) {
                // Manejo de errores adecuado
                e.printStackTrace()
            }
        }
    }
}
