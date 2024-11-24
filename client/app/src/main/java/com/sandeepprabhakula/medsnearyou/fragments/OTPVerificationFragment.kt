package com.sandeepprabhakula.medsnearyou.fragments

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.databinding.FragmentOTPVerificationBinding


class OTPVerificationFragment : Fragment() {

    private var _binding: FragmentOTPVerificationBinding? = null
    private val binding get() = _binding!!
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentOTPVerificationBinding.inflate(layoutInflater, container, false)
        val otpDigit1 = binding.otpDigit1
        val otpDigit2 = binding.otpDigit2
        val otpDigit3 = binding.otpDigit3
        val otpDigit4 = binding.otpDigit4
        setupOtpEditText(otpDigit1, null, otpDigit2)
        setupOtpEditText(otpDigit2, otpDigit1, otpDigit3)
        setupOtpEditText(otpDigit3, otpDigit2, otpDigit4)
        setupOtpEditText(otpDigit4, otpDigit3, null)
        binding.verifyOtpButton.setOnClickListener {
            val otp =
                otpDigit1.text.toString() + otpDigit2.text.toString() +
                        otpDigit3.text.toString() + otpDigit4.text.toString()
            when (otp) {
                "1234" -> {
        //                 TODO: verify otp and role, navigate to user home screen
                    findNavController().navigate(R.id.action_OTPVerificationFragment_to_userFragment)

                }
                "5678" -> {
        //                 TODO: verify otp and role, navigate to admin screen
                    findNavController().navigate(R.id.action_OTPVerificationFragment_to_vendorFragment)
                }
                else -> {
                    showBanner("Invalid OTP",false)
                }
            }
        }
        return binding.root
    }

    private fun setupOtpEditText(
        currentEditText: EditText,
        previousEditText: EditText?,
        nextEditText: EditText?
    ) {
        currentEditText.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable?) {
                // Move to the next EditText if a digit is entered
                if (s?.length == 1) {
                    nextEditText?.requestFocus()
                }
                // Move to the previous EditText if the field is empty
                else if (s?.isEmpty() == true) {
                    previousEditText?.requestFocus()
                }
            }

            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
        })
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