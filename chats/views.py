from django.views.generic import View
from django.shortcuts import render


class ChatView(View):
    template_name = "chats/index.html"

    def get(self, request):
        return render(request, self.template_name)