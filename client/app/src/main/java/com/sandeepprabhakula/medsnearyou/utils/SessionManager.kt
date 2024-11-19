package com.sandeepprabhakula.medsnearyou.utils

import android.content.Context
import android.content.SharedPreferences
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.dto.LoginResponseDTO

object SessionManager {
    const val USER_TOKEN = "user_token"

    /**
     * Function to save auth token
     */
    fun saveAuthToken(context: Context,loginResponseDTO: LoginResponseDTO) {
        saveString(context, loginResponseDTO)
    }

    /**
     * Function to fetch auth token
     */
    fun getToken(context: Context,key:String): String? {
        return getString(context, key)
    }

    fun saveString(context: Context, loginResponseDTO: LoginResponseDTO) {
        val prefs: SharedPreferences =
            context.getSharedPreferences(context.getString(R.string.app_name), Context.MODE_PRIVATE)
        val editor = prefs.edit()
        editor.putString("uid",loginResponseDTO.uid)
        editor.putString("token",loginResponseDTO.token)
        editor.putString("mobile",loginResponseDTO.mobile)
        editor.apply()

    }

    fun getString(context: Context, key: String): String? {
        val prefs: SharedPreferences =
            context.getSharedPreferences(context.getString(R.string.app_name), Context.MODE_PRIVATE)
        return prefs.getString(key, null)
    }

    fun clearData(context: Context){
        val editor = context.getSharedPreferences(context.getString(R.string.app_name), Context.MODE_PRIVATE).edit()
        editor.clear()
        editor.apply()
    }
}