package com.sandeepprabhakula.medsnearyou.repository

import com.sandeepprabhakula.medsnearyou.api.Medicine
import com.sandeepprabhakula.medsnearyou.utils.RetrofitClient

class MedicineRepository {
    private val apiService = RetrofitClient.createService<Medicine>()
}