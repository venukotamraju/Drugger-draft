from django.db import models

# Create your models here

# for list of medicines

class MedicineList(models.Model):
    medicine_id = models.BigAutoField("id of medicines",primary_key = True)
    medicine_name = models.CharField("name of the medicine", max_length = 50)

    def __str__(self):
        return self.medicine_name

# initiating categories
class CategoriesList(models.Model):
    category_id = models.BigAutoField("id of the respective category", primary_key = True)
    category_name = models.CharField("name of the category", max_length = 50)

    def __str__(self):
        return self.category_name

# mapping medicines to categories
class MedicineCategory(models.Model):
    medicine_id = models.OneToOneField("MedicineList",on_delete = models.CASCADE,primary_key=True,db_column = "medicine_id")
    category_id = models.OneToOneField("Categorieslist",on_delete = models.DO_NOTHING, blank = True, db_column = "category_id")

