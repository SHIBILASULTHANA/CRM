from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView,FormView
from django.urls import reverse_lazy
from .models import Board, List, Card
from .forms import BoardForm,ListForm
import json
from django.http import HttpResponseBadRequest

# Create your views here.

class ActivityView(TemplateView):
    template_name = 'web/admin/activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boards'] = Board.objects.all()

        # Serialize boards to JSON and pass it to the template
        boards_data = []
        for board in context['boards']:
            board_data = {
                'id': board.id,
                'name': board.name,
                'lists': []
            }
            for l in board.lists.all():
                list_data = {
                    'id': l.id,
                    'name': l.name,
                    # 'cards': [{'title': c.title, 'description': c.description} for c in l.cards.all()]
                }
                board_data['lists'].append(list_data)
            boards_data.append(board_data)
        context['boards_json'] = json.dumps(boards_data)

        return context

class CreateBoardView(CreateView):
    model = Board
    form_class = BoardForm
    template_name = 'web/admin/activity.html'
    success_url = reverse_lazy('activity:activity_view')

    def form_valid(self, form):
        if form.is_valid():
            print("Form is valid. Creating board...")
            response = super().form_valid(form)
            print("Board created successfully.")
            return response
        else:
            print("Form is invalid. Errors:", form.errors)
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Form is invalid. Errors:", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boards'] = Board.objects.all()
        return context
    
class CreateCardView(CreateView):
    model = Card
    fields = ['title', 'description']
    template_name = 'web/admin/activity.html'  # You might want to create a separate template for creating cards
    success_url = reverse_lazy('activity:activity_view')  # Redirect to the activity view after successful creation

    def form_valid(self, form):
        list_id = self.request.POST.get('list_id')
        try:
            list_instance = List.objects.get(id=list_id)
        except List.DoesNotExist:
            return HttpResponseBadRequest("Invalid list ID")

        form.instance.list = list_instance
        return super().form_valid(form)
    
class CreateListView(FormView):
    form_class = ListForm
    template_name = 'web/admin/activity.html'
    success_url = reverse_lazy('activity:activity_view')

    def form_valid(self, form):
        board_id = self.request.POST.get('board_id')
        board = Board.objects.get(id=board_id)
        list_name = form.cleaned_data['list_name']
        List.objects.create(name=list_name, board=board)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boards'] = Board.objects.all()
        return context
