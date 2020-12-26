from django.views.generic.base import TemplateView


class ContactsView(TemplateView):
    template_name = 'book/contacts.html'
