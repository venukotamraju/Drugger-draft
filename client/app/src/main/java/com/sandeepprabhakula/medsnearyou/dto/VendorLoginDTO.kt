package com.sandeepprabhakula.medsnearyou.dto

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class VendorLoginDTO(
    var email:String="",
    var role:String = ""
):Parcelable

