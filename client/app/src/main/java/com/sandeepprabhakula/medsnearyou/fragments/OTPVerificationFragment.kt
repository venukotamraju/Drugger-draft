package com.sandeepprabhakula.medsnearyou.fragments

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.databinding.FragmentOTPVerificationBinding
import com.sandeepprabhakula.medsnearyou.dto.CustomerLoginDTO
import com.sandeepprabhakula.medsnearyou.dto.LoginResponseDTO
import com.sandeepprabhakula.medsnearyou.utils.SessionManager


class OTPVerificationFragment : Fragment() {

    private var _binding: FragmentOTPVerificationBinding? = null
    private val binding get() = _binding!!
    private val args by navArgs<OTPVerificationFragmentArgs>()
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentOTPVerificationBinding.inflate(layoutInflater, container, false)
        val otpDigit1 = binding.otpDigit1
        val otpDigit2 = binding.otpDigit2
        val otpDigit3 = binding.otpDigit3
        val otpDigit4 = binding.otpDigit4
        val otpDigit5 = binding.otpDigit5
        val otpDigit6 = binding.otpDigit6
        setupOtpEditText(otpDigit1, null, otpDigit2)
        setupOtpEditText(otpDigit2, otpDigit1, otpDigit3)
        setupOtpEditText(otpDigit3, otpDigit2, otpDigit4)
        setupOtpEditText(otpDigit4, otpDigit3, otpDigit5)
        setupOtpEditText(otpDigit5, otpDigit4, otpDigit6)
        setupOtpEditText(otpDigit6, otpDigit5, null)

        binding.verifyOtpButton.setOnClickListener {
            val otp =
                otpDigit1.text.toString() + otpDigit2.text.toString() +
                        otpDigit3.text.toString() + otpDigit4.text.toString() + otpDigit5.text.toString() + otpDigit6.text.toString()
            when (otp) {
                "123456" -> {
                    //                 TODO: verify otp and role, navigate to user home screen
                    if (args.customerLogin.role == "ROLE_USER" && args.vendorLogin.role == "") {
                        Log.d("LOGGED_IN_AS", "user")
                        findNavController().navigate(R.id.action_OTPVerificationFragment_to_userFragment)
//                        TODO: Store the role and token in shared preferences
                        SessionManager.saveString(
                            requireContext(),
                            LoginResponseDTO("dummy", "1234567890", "test", "", "ROLE_USER")
                        )
                    } else {
                        Log.d("LOGGED_IN_AS", "vendor")
                        findNavController().navigate(R.id.action_OTPVerificationFragment_to_vendorFragment)
                        //                        TODO: Store the role and token in shared preferences
                        SessionManager.saveString(
                            requireContext(),
                            LoginResponseDTO(
                                "dummy",
                                "",
                                "testVendor",
                                "vendor@wall.com",
                                "ROLE_VENDOR"
                            )
                        )
                    }

                }

//                "234567" -> {
//                    //                 TODO: verify otp and role, navigate to admin screen
//                    findNavController().navigate(R.id.action_OTPVerificationFragment_to_vendorFragment)
//                }

                else -> {
                    showBanner("Invalid OTP", false)
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
                when {
                    // Move to the next EditText if a digit is entered
                    s?.length == 1 -> nextEditText?.requestFocus()

                    // Move to the previous EditText if the field is empty (on backspace)
                    s.isNullOrEmpty() && previousEditText != null -> previousEditText.requestFocus()
                }
            }

            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
        })
        currentEditText.setOnKeyListener { _, keyCode, event ->
            if (keyCode == KeyEvent.KEYCODE_DEL && event.action == KeyEvent.ACTION_DOWN && currentEditText.text.isEmpty()) {
                previousEditText?.requestFocus()
                true
            } else {
                false
            }
        }
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