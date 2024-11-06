from django.shortcuts import render,redirect
from django.views.generic import View
from store.forms import VehicleForm,VehicleUpdateForm
from store.models import Vehicle
from django.db.models import Q


class VehicleCreateView(View):
    template_name="vehicle_add.html"
    form_class=VehicleForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data,files=request.FILES)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            print(data)
            Vehicle.objects.create(**data)  
            return redirect("vehicle-list")
        return render(request,self.template_name,{"form":form_instance})

class VehicleListView(View):
    template_name="vehicle_list.html"
    def get(self,request,*args,**kwargs):
        search_text=request.GET.get("filter")
        qs=Vehicle.objects.all()
        all_names=Vehicle.objects.values_list("name",flat=True).distinct()
        all_brands=Vehicle.objects.values_list("brand",flat=True).distinct()
        all_fuel_type=Vehicle.objects.values_list("fuel_type",flat=True).distinct()
        all_owner_type=Vehicle.objects.values_list("owner_type",flat=True).distinct()
        all_records=[]
        all_records.extend(all_names)
        all_records.extend(all_brands)
        all_records.extend(all_fuel_type)
        all_records.extend(all_owner_type)
        if search_text:
            qs=qs.filter(
                Q(name__contains=search_text)|
                Q(fuel_type__contains=search_text)|
                Q(owner_type__contains=search_text)|
                Q(brand__contains=search_text)
                )
        return render(request,self.template_name,{"data":qs,"records":all_records})
        
class VehicleDetailView(View):
    template_name="vehicle_detail.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Vehicle.objects.get(id=id)
        return render(request,self.template_name,{"data":qs})

class VehicleDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Vehicle.objects.get(id=id).delete()
        return redirect("vehicle-list")

# class VehicleUpdateView(View):
#     template_name="vehicle_update.html"
#     form_class=VehicleForm
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         vehicle_objects=Vehicle.objects.get(id=id)
#         data={
#             "name":vehicle_objects.name,
#             "varient":vehicle_objects.varient,
#             "description":vehicle_objects.description,
#             "fuel_type":vehicle_objects.fuel_type,
#             "running_km":vehicle_objects.running_km,
#             "color":vehicle_objects.color,
#             "price":vehicle_objects.price,
#             "brand":vehicle_objects.brand,
#             "qwner_type":vehicle_objects.owner_type        
#         }
#         form_instance=self.form_class(initial=data)
#         return render(request,self.template_name,{"form":form_instance})
#     def post(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         form_data=request.POST
#         form_instance=self.form_class(form_data,files=request.FILES)
#         if form_instance.is_valid():
#             data=form_instance.cleaned_data
#             Vehicle.objects.filter(id=id).update(**data)
#             return redirect("vehicle-list")
#         return render(request,self.template_name,{"form":form_instance})

class VehicleUpdateView(View):
    template_name="vehicle_update.html"
    form_class=VehicleUpdateForm
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        vehicle_object=Vehicle.objects.get(id=id)
        form_instance=self.form_class(instance=vehicle_object)
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        vehicle_object=Vehicle.objects.get(id=id)
        form_data=request.POST
        form_instance=self.form_class(form_data,files=request.FILES,instance=vehicle_object)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("vehicle-list")
        return render(request,self.template_name,{"form":form_instance})

