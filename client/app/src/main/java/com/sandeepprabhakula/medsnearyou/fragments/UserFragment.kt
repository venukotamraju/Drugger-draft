package com.sandeepprabhakula.medsnearyou.fragments

import android.location.Location
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.google.android.material.slider.Slider
import com.sandeepprabhakula.medsnearyou.databinding.FragmentUserBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.launch

class UserFragment : Fragment() {
    private var _binding: FragmentUserBinding? = null
    private val binding get() = _binding!!
    private val searchQuery = MutableStateFlow("")

    private val searchScope = CoroutineScope(Dispatchers.Main + Job())
    @OptIn(FlowPreview::class)
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentUserBinding.inflate(layoutInflater, container, false)
        binding.userSearchView.setupWithSearchBar(binding.searchBar)


        val searchEditText = binding.userSearchView.editText
        searchEditText.addTextChangedListener(object:TextWatcher{
            override fun beforeTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
                Log.d("before",p0.toString())
            }

            override fun onTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
                searchQuery.value = p0.toString()
            }

            override fun afterTextChanged(p0: Editable?) {
                Log.d("after",p0.toString())
            }

        })
        searchScope.launch {
            searchQuery
                .debounce(500) // 500ms delay
                .filter { it.isNotEmpty() } // Only hit API if the text is not empty
                .distinctUntilChanged() // Only trigger if the text is different from last
                .collect { query ->
                    Log.d("SEARCHED_LOGS",query)
//                    TODO: Make an API call to search Endpoint
//                    refer this url for populating recyclerview: https://chatgpt.com/c/6721a1c5-020c-8012-a6bb-2becadae9019
//                    fetchSearchResults(query)
                }
        }
        binding.distanceSeekBar.addOnSliderTouchListener(object: Slider.OnSliderTouchListener{
            override fun onStartTrackingTouch(slider: Slider) {
                binding.radiusKms.text = "Search with in ${slider.value} Kms."
                Log.d("Slider_KMS",slider.value.toString())
            }

            override fun onStopTrackingTouch(slider: Slider) {
                val radius = slider.value
                binding.radiusKms.text = "Search with in ${Math.floor(slider.value.toDouble()).toInt()} Kms."
//                TODO: Make API call for changing the data in RecyclerView
                Log.d("Slider_KMS",radius.toString())
            }

        })
        return binding.root
    }

//    private fun fetchSearchResults(query: String) {
//        // Simulate an API call with Coroutine (replace with actual API call)
//        searchScope.launch {
//            val results = apiCall(query) // Replace with your API call method
//            updateRecyclerView(results)
//        }
//    }
//    private suspend fun apiCall(query: String): List<SearchResult> {
//        // Simulate delay for API call (replace with your API request)
//        delay(1000)
//        return listOf(
//            SearchResult("Result 1 for $query", "Description 1"),
//            SearchResult("Result 2 for $query", "Description 2")
//        )
//    }
//    private fun updateRecyclerView(results: List<SearchResult>) {
//        searchResultAdapter.updateResults(results)
//        searchResultsRecyclerView.visibility = if (results.isNotEmpty()) View.VISIBLE else View.GONE
//    }
    
    override fun onDestroy() {
        super.onDestroy()
        searchScope.cancel()
    }

    fun calculateDistance(
        startLatitude: Double,
        startLongitude: Double,
        endLatitude: Double,
        endLongitude: Double
    ): Float {
        val startLocation = Location("Start").apply {
            latitude = startLatitude
            longitude = startLongitude
        }

        val endLocation = Location("End").apply {
            latitude = endLatitude
            longitude = endLongitude
        }

        // Calculate distance in meters
        return startLocation.distanceTo(endLocation)
    }

}