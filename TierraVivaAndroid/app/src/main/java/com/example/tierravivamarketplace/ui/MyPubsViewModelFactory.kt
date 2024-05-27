package com.example.tierravivamarketplace.ui

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider

class MyPubsViewModelFactory(private val context: Context) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(MyPubsViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return MyPubsViewModel(context) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
