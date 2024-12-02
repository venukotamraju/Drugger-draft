package com.sandeepprabhakula.medsnearyou.api

import retrofit2.http.GET

interface Vendor {
    @GET("api/v1/vendor")
    fun getVendor()
}