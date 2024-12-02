package com.sandeepprabhakula.medsnearyou.api

import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface Customer {
    @GET("api/v1/customers")
    fun getCustomer()

    @POST("api/v1/customers/customerlist")
    fun createCustomer()

    @GET("api/v1/customers/customerlist")
    fun getCustomerList()

    @PUT("api/v1/customers/customerlist")
    fun updateCustomer()

    @DELETE("api/v1/customers/customerlist")
    fun deleteCustomer()

    @GET("api/v1/customers/customerdetails/{uid}")
    fun getCustomerDetails(@Path("uid") uid:Int)

    @POST("api/v1/customers/customerverification/{uid}/generate-otp/")
    fun generateOTP(@Path("uid")uid:Int)

    @POST("api/v1/customers/customerverification/{uid}/validate-otp/")
    fun validateOTP(@Path("uid")uid:Int)

}