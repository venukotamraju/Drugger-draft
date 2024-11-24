package com.sandeepprabhakula.medsnearyou.fragments

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.findNavController
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.databinding.FragmentLauncherBinding


class LauncherFragment : Fragment() {
    private var _binding:FragmentLauncherBinding? = null
    private val binding get() = _binding!!
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentLauncherBinding.inflate(inflater,container,false)
        binding.customerCard.setOnClickListener {
            findNavController().navigate(R.id.action_launcherFragment_to_loginFragment)
        }
        binding.vendorCard.setOnClickListener {
            findNavController().navigate(R.id.action_launcherFragment_to_vendorLoginFragment)
        }
        return binding.root
    }

}