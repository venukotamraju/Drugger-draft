package com.sandeepprabhakula.medsnearyou.utils

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.util.Log
import android.widget.Toast

class NetworkMonitor(private val context:Context){
    private val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    private var isConnected: Boolean = false
    private val networkCallback = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
            super.onAvailable(network)
            isConnected = true
            // Handle network available
            Log.d("NETWORK_LOGS","Connected")
            onNetworkStatusChanged(isConnected)
        }

        override fun onLost(network: Network) {
            super.onLost(network)
            isConnected = false
            Log.d("NETWORK_LOGS","Disconnected")
            Toast.makeText(context,"Network Lost",Toast.LENGTH_SHORT).show()
            onNetworkStatusChanged(isConnected)
        }
    }
    fun startNetworkCallback() {
        try{
            val networkRequest = NetworkRequest.Builder()
                .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
                .addTransportType(NetworkCapabilities.TRANSPORT_CELLULAR)
                .build()
            connectivityManager.requestNetwork(networkRequest, networkCallback)
        }catch (e:Exception){
            Log.d("NETWORK_LOGS",e.message.toString())
        }


    }
    fun stopNetworkCallback() {
        connectivityManager.unregisterNetworkCallback(networkCallback)
    }
    private fun onNetworkStatusChanged(isConnected: Boolean) {
        // Update your UI or notify listeners here
        if (isConnected) {
            Log.d("NETWORK_CONNECTED","Connected to the internet.")
        } else {
            Log.d("NETWORK_DISCONNECTED","Disconnected from the internet.")
        }
    }
}