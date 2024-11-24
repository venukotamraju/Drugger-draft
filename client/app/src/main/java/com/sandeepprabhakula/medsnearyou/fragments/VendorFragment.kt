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
        binding.categoryChip.setOnClickListener {
            showBottomSheet()
        }
        return binding.root
    }
    private fun showBottomSheet(){
        val bottomDialogSheet = BottomSheetDialog(requireContext())
        val view = layoutInflater.inflate(R.layout.filter_vendor_bottom_sheet, null)
        bottomDialogSheet.setContentView(view)
        val allCategories:CheckBox = view.findViewById(R.id.allCategories)
        val categoryA:CheckBox = view.findViewById(R.id.categoryA)
        val categoryB:CheckBox = view.findViewById(R.id.categoryB)
        val categoryC:CheckBox = view.findViewById(R.id.categoryC)
        val categoryD:CheckBox = view.findViewById(R.id.categoryD)
        val filterBtn:Button = view.findViewById(R.id.submitCategoryFilterBtn)
        val selectedCategories = mutableListOf<String>()
        filterBtn.setOnClickListener {
            if(categoryA.isChecked) {
                selectedCategories.add(categoryA.text.toString())
                allCategories.isChecked = false
            }
            if(categoryB.isChecked) {
                selectedCategories.add(categoryB.text.toString())
                allCategories.isChecked = false
            }
            if(categoryC.isChecked) {
                selectedCategories.add(categoryC.text.toString())
                allCategories.isChecked = false
            }
            if(categoryD.isChecked) {
                selectedCategories.add(categoryD.text.toString())
                allCategories.isChecked = false
            }
            if(selectedCategories.size==0) selectedCategories.add(0,"All")
            populateChipGroup(selectedCategories)
            bottomDialogSheet.dismiss()
        }
        bottomDialogSheet.show()
    }

    private fun populateChipGroup(categories:List<String>){
        for(category in categories){
            val existingDistanceChip =
                binding.filteredMedicineChipGroup.children.find { (it as Chip).text.contains(category) }
            if (existingDistanceChip != null) binding.filteredMedicineChipGroup.removeView(existingDistanceChip)
            addChipToGroup(category)
        }
    }
    private fun addChipToGroup(text: String) {
        val chip = Chip(requireContext()).apply {
            this.text = text
            isCloseIconVisible = true // Show a close icon for removal
            setOnCloseIconClickListener {
                binding.filteredMedicineChipGroup.removeView(this) // Remove chip on close icon click
            }
        }
        binding.filteredMedicineChipGroup.addView(chip)
    }
}