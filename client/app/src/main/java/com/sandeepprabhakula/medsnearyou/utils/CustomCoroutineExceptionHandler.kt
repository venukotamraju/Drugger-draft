package com.sandeepprabhakula.medsnearyou.utils

import android.content.Context
import android.util.Log
import android.widget.Toast
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.launch
import java.net.UnknownHostException

class CustomCoroutineExceptionHandler(private val context: Context) {
    val exceptionHandler = CoroutineExceptionHandler { _, exception ->
        when (exception) {
            is UnknownHostException -> {
                MainScope().launch {
                    Toast.makeText(
                        context,
                        "Please check your network connection",
                        Toast.LENGTH_LONG
                    ).show()
                    Log.e("NETWORK_LOGS", "Caught ${exception.message}")
                }
            }

            else -> {
                MainScope().launch {
                    Toast.makeText(context, "Unknown error occurred", Toast.LENGTH_LONG).show()
                    Log.d("CoroutineError", "Caught ${exception.message}")
                }
            }
        }
    }
}