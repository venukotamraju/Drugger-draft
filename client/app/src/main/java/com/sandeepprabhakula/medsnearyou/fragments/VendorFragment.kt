package com.sandeepprabhakula.medsnearyou.fragments

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.databinding.FragmentVendorBinding


class VendorFragment : Fragment() {
    private var _binding:FragmentVendorBinding? = null
    private val binding get() = _binding!!
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentVendorBinding.inflate(layoutInflater,container,false)
        
        return binding.root
    }
}