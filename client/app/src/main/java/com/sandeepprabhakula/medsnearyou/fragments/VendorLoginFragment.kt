package com.sandeepprabhakula.medsnearyou.fragments

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.databinding.FragmentVendorLoginBinding


class VendorLoginFragment : Fragment() {
    private var _binding: FragmentVendorLoginBinding? = null
    private val binding get() = _binding!!
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentVendorLoginBinding.inflate(inflater, container, false)
        binding.sendOtpButton.setOnClickListener {
            val isValidEmail = isEmailValid(binding.registeredVendorEmail.text.toString().trim())
            if (!isValidEmail) {
                showBanner("Please provide valid email address", false)
            } else {
                findNavController().navigate(R.id.action_vendorLoginFragment_to_OTPVerificationFragment)
            }
        }

        return binding.root
    }

    private fun isEmailValid(email: String): Boolean {
        return android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()
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