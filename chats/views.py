from django.shortcuts import render
from django.views.generic import View


class ChatView(View):
    template_name = "chats/page.html"

    def get(self, request):
        return render(request, self.template_name)
