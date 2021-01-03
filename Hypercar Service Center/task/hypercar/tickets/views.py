from django.views import View
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render
from collections import deque


class ServiceManager:
    change_oil = "change_oil"
    inflate_tires = "inflate_tires"
    diagnostic = "diagnostic"
    oil_time = 2
    tires_time = 5
    diagnostic_time = 30
    current_ticket = 0

    menu = [
        {"name": "Change oil", "path": change_oil},
        {"name": "Inflate tires", "path": inflate_tires},
        {"name": "Get diagnostic test", "path": diagnostic},
    ]

    clients = {
        change_oil: deque(),
        inflate_tires: deque(),
        diagnostic: deque(),
    }

    def get_ticket(self):
        ticket = self.current_ticket + 1
        self.current_ticket += 1
        return ticket

    def get_wait_time(self, operation):
        _wait_time = len(self.clients[self.change_oil]) * self.oil_time
        if operation == self.change_oil:
            return _wait_time

        _wait_time += len(self.clients[self.inflate_tires]) * self.tires_time
        if operation == self.inflate_tires:
            return _wait_time

        _wait_time += len(self.clients[self.diagnostic]) * self.diagnostic_time
        return _wait_time

    def add_to_queue(self, request_path):
        filter_path = list(filter(None, request_path.split('/')))
        operation = filter_path[-1]
        client = {
            "ticket": self.get_ticket(),
            "wait_time": self.get_wait_time(operation),
            "operation": operation
        }

        self.clients[operation].appendleft(client)
        return client


manager = ServiceManager()


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(TemplateView):
    template_name = 'tickets/menu.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'menu': manager.menu})


class TicketView(TemplateView):
    template_name = 'tickets/client_ticket.html'
    client = {}

    def get(self, request, *args, **kwargs):
        self.client = manager.add_to_queue(request.path)
        return render(request, self.template_name, {'client': self.client})
