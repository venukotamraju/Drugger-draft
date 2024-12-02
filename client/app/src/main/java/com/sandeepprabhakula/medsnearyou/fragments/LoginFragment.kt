package com.sandeepprabhakula.medsnearyou.fragments

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.findNavController
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.databinding.FragmentLoginBinding
import com.sandeepprabhakula.medsnearyou.dto.CustomerLoginDTO
import com.sandeepprabhakula.medsnearyou.dto.VendorLoginDTO

class LoginFragment : Fragment() {
    private var _binding: FragmentLoginBinding? = null
    private val binding get() = _binding!!
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        _binding = FragmentLoginBinding.inflate(layoutInflater, container, false)
        binding.sendOtpButton.setOnClickListener {
//            TODO: API Call for generating and sending OTP
            val mobileNumber = binding.registeredMobile.text.toString()
            if (mobileNumber.length != 10 || mobileNumber.length > 10) {
                showBanner("Invalid mobile number", false)
            } else {
//                showBanner("OTP sent to the mobile number", true)
                val action = LoginFragmentDirections.actionLoginFragmentToOTPVerificationFragment(
                    CustomerLoginDTO(mobileNumber,"ROLE_USER"),VendorLoginDTO()
                )
                findNavController().navigate(action)
            }
        }
        return binding.root
    }

    private fun showBanner(message: String, isSuccess: Boolean) {
        with(binding.banner.root) {
            visibility = View.VISIBLE
            setBackgroundColor(
                if (isSuccess) resources.getColor(R.color.green) else resources.getColor(
                    R.color.red
                )
            )
        }

        binding.banner.bannerMessage.text = message

        // Hide the banner after 2 seconds

        Handler(Looper.getMainLooper()).postDelayed({
            binding.banner.root.visibility = View.GONE
        }, 3000)
    }


}