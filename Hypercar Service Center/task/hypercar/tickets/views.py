from django.views import View
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque


class Operation:
    def __init__(self, identifier, name, time, queue_description = ""):
        self.identifier = identifier
        self.name = name
        self.time = time
        self.queue_description = self.name if queue_description == "" else queue_description
        self.queue_description += " queue"


class ServiceManager:
    change_oil = Operation("change_oil", "Change oil", 2)
    inflate_tires = Operation("inflate_tires", "Inflate tires", 5)
    diagnostic = Operation("diagnostic", "Get diagnostic test", 30, "Get diagnostic")
    current_ticket = 0
    next_client = None

    menu = [
        {"name": change_oil.name, "path": change_oil.identifier},
        {"name": inflate_tires.name, "path": inflate_tires.identifier},
        {"name": diagnostic.name, "path": diagnostic.identifier},
    ]

    clients = {
        change_oil.identifier: deque(),
        inflate_tires.identifier: deque(),
        diagnostic.identifier: deque(),
    }

    def get_ticket(self):
        ticket = self.current_ticket + 1
        self.current_ticket += 1
        return ticket

    def get_wait_time(self, operation):
        _wait_time = len(self.clients[self.change_oil.identifier]) * self.change_oil.time
        if operation == self.change_oil.identifier:
            return _wait_time

        _wait_time += len(self.clients[self.inflate_tires.identifier]) * self.inflate_tires.time
        if operation == self.inflate_tires.identifier:
            return _wait_time

        _wait_time += len(self.clients[self.diagnostic.identifier]) * self.diagnostic.time
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

    def get_status(self):
        status = [
            {"description": self.change_oil.queue_description, "count": len(self.clients[self.change_oil.identifier])},
            {"description": self.inflate_tires.queue_description, "count": len(self.clients[self.inflate_tires.identifier])},
            {"description": self.diagnostic.queue_description, "count": len(self.clients[self.diagnostic.identifier])},
        ]
        return status

    def get_next_client(self):
        if self.next_client is None:
            return "Waiting for the next client"
        else:
            ticket = self.next_client["ticket"]
            return f"Next ticket #{ticket}"

    def call_next_client(self):
        if len(self.clients[self.change_oil.identifier]) > 0:
            self.next_client = self.clients[self.change_oil.identifier].pop()
        elif len(self.clients[self.inflate_tires.identifier]) > 0:
            self.next_client = self.clients[self.inflate_tires.identifier].pop()
        elif len(self.clients[self.diagnostic.identifier]) > 0:
            self.next_client = self.clients[self.diagnostic.identifier].pop()
        else:
            self.next_client = None


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


class ControlView(TemplateView):
    template_name = 'tickets/control.html'
    status = []

    def get(self, request, *args, **kwargs):
        self.status = manager.get_status()
        return render(request, self.template_name, {'status': self.status})

    def post(self, request, *args, **kwargs):
        manager.call_next_client()
        return redirect('/processing')


class NextClientView(TemplateView):
    template_name = 'tickets/next_client.html'
    client = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'message': manager.get_next_client()})
