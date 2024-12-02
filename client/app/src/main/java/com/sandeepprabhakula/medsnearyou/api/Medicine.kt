package com.sandeepprabhakula.medsnearyou.api

import retrofit2.http.GET

interface Medicine {
    @GET("api/v1/medicines/")
    fun getMedicine()
}