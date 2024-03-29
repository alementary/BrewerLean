import sys
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime, timedelta
from django.http import request
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import TemplateView
from delivery.models.delivery_models import DeliveryMetrics
from delivery.forms.delivery_forms import DeliveryForm


class CreateDeliveryMetricsView(CreateView, LoginRequiredMixin):
    model = DeliveryMetrics
    template_name = 'delivery/create-delivery-metrics.html'
    form_class = DeliveryForm
    success_url = '/delivery/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Create Delivery'
        return context


class UpdateDeliveryMetricsView(UpdateView, LoginRequiredMixin):
    model = DeliveryMetrics
    template_name = 'delivery/create-delivery-metrics.html'
    form_class = DeliveryForm
    success_url = '/delivery/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Update Delivery'
        return context


class DeliveryMetricsListView(ListView, LoginRequiredMixin):
    model = DeliveryMetrics
    paginate_by = 10
    template_name = 'delivery/home.html'
    context_object_name = 'metrics'

    def get_queryset(self):
        return DeliveryMetrics.objects.all().order_by('-delivery_date')

    def get_context_data(self, **kwargs):
        context = super(DeliveryMetricsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Delivery Metrics'
        deliveries = DeliveryMetrics.objects.all().order_by('-delivery_date')
        return context