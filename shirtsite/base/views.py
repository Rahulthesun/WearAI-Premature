import os
from typing import Any
import openai
import requests

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse , HttpResponseRedirect




from django.contrib.auth import login,authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django.views.generic import FormView,UpdateView , ListView,DetailView
from django.contrib.auth.forms import UserCreationForm

from django.views.generic.edit import CreateView
from .models import Order,imageui


openai.api_key = "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"
imgbb_key = '4293ead9e871a798ed6d0580bb00f15c'
upload_url = 'https://api.imgbb.com/1/upload'



# Create your views here.

class UserLoginView(LoginView):
    redirect_authenticated_user=True
    fields='__all__'
    template_name='base/loginform.html'


    def get_success_url(self):
        return reverse_lazy('design')
    
class UserRegistration(FormView):
    form_class=UserCreationForm
    redirect_authenticated_user=True
    template_name='base/register.html'
    success_url=reverse_lazy('design_list')

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request , user)
        return super(UserRegistration,self).form_valid(form)
            
        


def home_test(request):
    surl=reverse_lazy('design_list')
    context={'url':surl}
    return render(request,'base/home.html',context)

@login_required()
def design(request):
    try:
        obj=imageui.objects.get(user=request.user)
        orders=Order.objects.get(image=obj)

    except ObjectDoesNotExist:
        orders=None
    
    if orders is None:
        url= reverse_lazy('size')
    else:
        url=reverse_lazy('order_summary')
        
    obj=imageui.objects.get(user=request.user) 
    img_url = obj.url
    logout_url=reverse_lazy('logout')
    context={
        'obj':obj,
        'url':url,
        'l_url': logout_url,
        'i_url': img_url
             }
    return render(request,'base/design.html',context)


class SizeCreateView(LoginRequiredMixin,CreateView):
    model=Order
    fields=['size','name','email','phone','address']
    template_name='base/form.html'
    success_url = reverse_lazy('order_summary')

    #def get(self,request,*args,**kwargs):
        #if Order.objects.filter(user=self.request.user).exists():
           # r_path=reverse_lazy('order_summary')
            #return redirect(r_path)
        #else:
            #pass

    def form_valid(self,form):
        order=form.save(commit=False)
        img = imageui.objects.get(user=self.request.user)
        order.image = img
        order.save()
        return super(SizeCreateView,self).form_valid(form)
    
class UpdateOrderInfo(LoginRequiredMixin,UpdateView):
    model=Order
    fields=['size','name','email','phone','address']
    template_name = 'base/form_edit.html'
    success_url = reverse_lazy('order_summary')


@login_required()
def OrderDetails(request):
    obj = imageui.objects.get(user = request.user)
    img_url=obj.url
    order_d= Order.objects.get(image=obj)
    surl=reverse_lazy('payment')
    edit_url = reverse_lazy('size_edit')
    context={
        'img_url': img_url,
        'obj': obj,
        'order': order_d,
        'url':surl,
        'e_url': edit_url
    }
    return render(request , 'base/order_summary.html',context)

@login_required()
def PaymentGateway(request):
    return HttpResponse("PAYMENT GATEWAY")

@login_required()
def Aidesign(request):
    res = imageui.objects.get(user=request.user)
    prompt_text = res.request

    prompt= prompt_text
    next_url=reverse_lazy('design')
    response = openai.Image.create(
              prompt=prompt,
              n=1,
              size="1024x1024",
              response_format='url',
              )
    image_url = response['data'][0]['url']
    payload = {
    'key': imgbb_key,
    'image': image_url
    }
    response = requests.post(upload_url, data=payload)
    result = response.json()
    image_url_refined =result['data']['url']
    res.url=image_url_refined
    res.save()
    context={
      'res': res,
      'i_url': image_url,
      'next_url': next_url
    }
    
    return render(request,'base/aides.html',context)



class ImageRequestView(LoginRequiredMixin,CreateView):
    model=imageui
    fields=['request']
    template_name='base/aires.html'
    success_url = reverse_lazy('aides') #change this to aides
    
    def form_valid(self,form):
        order_det = form.save(commit=False)
        order_det.user = self.request.user
        order_det.save()
        return super().form_valid(form)


class UpdateImageRequest(LoginRequiredMixin,UpdateView):
    model=imageui
    fields=['request']
    template_name = 'base/aires.html'
    success_url = reverse_lazy('aides')
    
class DesignList(ListView):
    model=imageui
    context_object_name = 'designs'
    template_name = 'base/design_list.html'

'''
def DesignDetailView(request,pk):
    obj = imageui.objects.get(id=pk)

    context={
        'obj': obj
    }
    return render(request,template_name='base/design_edit.html',context=context)

    
'''

