package com.sandeepprabhakula.medsnearyou.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.cardview.widget.CardView
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.recyclerview.widget.RecyclerView
import com.sandeepprabhakula.medsnearyou.R
import com.sandeepprabhakula.medsnearyou.tempDto.SearchDTO

class SearchedAdapter(private val listener:ViewDetails): RecyclerView.Adapter<SearchedAdapter.SearchViewHolder>() {
    private var searchList = mutableListOf<SearchDTO>()
    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): SearchViewHolder {
        val view = SearchViewHolder(LayoutInflater.from(parent.context).inflate(R.layout.searched_medicine_layout, parent, false))
        view.searchedMedicineCard
            .setOnClickListener {
            listener.onCardClicked(searchList[view.adapterPosition])
        }
        return view
    }

    class SearchViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val searchedMedicneText: TextView = itemView.findViewById(R.id.searchedMedicineName)
        val searchedMedicneVendor: TextView = itemView.findViewById(R.id.searchedVendorName)
        val distance: TextView = itemView.findViewById(R.id.searchedMedicineDistance)
        val searchedMedicineCard: CardView = itemView.findViewById(R.id.searchedMedicineCard)
    }

    override fun onBindViewHolder(holder: SearchViewHolder, position: Int) {
        val currentItem = searchList[position]
        holder.searchedMedicneText.text = currentItem.medicineName
        holder.searchedMedicneVendor.text = currentItem.medicineVendor
        holder.distance.text = currentItem.distance
    }
    fun setData(searchList:MutableList<SearchDTO>){
        this.searchList = searchList
        notifyDataSetChanged()
    }
    override fun getItemCount(): Int {
        return searchList.size
    }
    interface ViewDetails{
        fun onCardClicked(searchedDTO:SearchDTO)
    }
}