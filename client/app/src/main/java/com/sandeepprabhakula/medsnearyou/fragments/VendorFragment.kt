package com.sandeepprabhakula.medsnearyou.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.CheckBox
import androidx.core.view.children
import androidx.fragment.app.Fragment
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.android.material.chip.Chip
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
        binding.vendorSearchView.setupWithSearchBar(binding.vendorSearchBar)
        return binding.root
    }

}