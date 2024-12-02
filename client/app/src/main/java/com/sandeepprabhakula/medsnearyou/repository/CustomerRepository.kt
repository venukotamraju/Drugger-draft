package com.sandeepprabhakula.medsnearyou.repository

import com.sandeepprabhakula.medsnearyou.api.Customer
import com.sandeepprabhakula.medsnearyou.utils.RetrofitClient

class CustomerRepository {
    private val apiService = RetrofitClient.createService<Customer>()
}