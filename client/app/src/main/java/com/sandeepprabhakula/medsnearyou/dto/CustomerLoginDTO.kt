package com.sandeepprabhakula.medsnearyou.dto

import android.os.Parcelable
import kotlinx.parcelize.Parcelize


@Parcelize
data class CustomerLoginDTO(
    var mobile:String = "",
    val role:String = "ROLE_USER"
): Parcelable
