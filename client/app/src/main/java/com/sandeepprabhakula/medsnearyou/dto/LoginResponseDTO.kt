package com.sandeepprabhakula.medsnearyou.dto

data class LoginResponseDTO (
    var uid:String="",
    var mobile:String = "",
    var token:String="",
    var email:String="",
    var role:String=""
)