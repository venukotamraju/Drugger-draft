package com.sandeepprabhakula.medsnearyou.repository

import com.sandeepprabhakula.medsnearyou.api.Vendor
import com.sandeepprabhakula.medsnearyou.utils.RetrofitClient

class VendorRepository {
    private val apiService = RetrofitClient.createService<Vendor>()
}