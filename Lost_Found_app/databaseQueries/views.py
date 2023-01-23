from django.views.generic import DetailView
from databaseQueries.models import Announcement


class EmpImageDisplay(DetailView):
    model = Announcement
    template_name = 'renderAnnIMG.html'
    context_object_name = 'annModel'