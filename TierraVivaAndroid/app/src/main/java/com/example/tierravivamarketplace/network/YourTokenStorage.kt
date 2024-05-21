package com.example.tierravivamarketplace.network

import android.content.Context
import android.content.SharedPreferences

object YourTokenStorage {
    private const val PREF_NAME = "MyAppPrefs"
    private const val TOKEN_KEY = "token"

    private fun getPreferences(context: Context): SharedPreferences {
        return context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
    }

    fun saveToken(token: String?, context: Context) {
        val prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
        val editor = prefs.edit()
        editor.putString(TOKEN_KEY, token)
        editor.apply()
    }

    fun getToken(context: Context): String? {
        val prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
        return prefs.getString(TOKEN_KEY, null)
    }
}