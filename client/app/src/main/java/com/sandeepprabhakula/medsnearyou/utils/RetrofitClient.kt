package com.sandeepprabhakula.medsnearyou.utils

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    private const val BASE_URL = "http://127.0.0.1:8000/"
    val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    inline fun <reified T> createService(): T {
        return retrofit.create(T::class.java)
    }
}