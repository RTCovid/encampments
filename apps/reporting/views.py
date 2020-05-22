import django_tables2 as tables
from django.views.generic import CreateView
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.reporting.models import Encampment
from apps.reporting.models import Organization
from apps.reporting.models import Report
from apps.reporting.models import Task
from apps.reporting.serializers import EncampmentSerializer
from apps.reporting.serializers import OrganizationSerializer
from apps.reporting.serializers import ReportSerializer


class EncampmentListView(ListView):
    model = Encampment

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            "not_visited_14": Encampment.not_visited_in(14).count(),
            "visits_7": Report.last_n(7).count(),
            "visits_31": Report.last_n(31).count(),
            "pending_tasks": Task.objects.filter(completed=None).count(),
            "table": EncampmentTable(self.object_list),
        }
        return {**context, **extra_context}


class HybridDate(tables.Column):
    pass


class EncampmentTable(tables.Table):
    name = tables.Column(linkify=True)
    location = tables.Column()

    last_visit = HybridDate(accessor="last_report.date")
    next_visit = HybridDate(accessor="next_visit.date")

    tasks = tables.Column(accessor="open_tasks.count")


# TODO: admin permissions
class EncampmentCreateView(CreateView):
    model = Encampment
    fields = ["name", "locations_geom"]


class ReportListView(ListView):
    model = Report

    def get_queryset(self):
        return Report.objects.filter(encampment=self.kwargs["encampment"]).order_by(
            "-date"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["encampment"] = Encampment.objects.get(id=self.kwargs["encampment"])
        return context


class OrganizationCreateView(CreateView):
    model = Organization
    fields = ["name"]


class ReportCreateView(CreateView):
    model = Report

    fields = [
        "date",
        "encampment",
        "recorded_location",
        "performed_by",
        "supplies_delivered",
        "food_delivered",
        "occupancy",
        "talked_to",
        "assessed",
        "assessed_asymptomatic",
        "needs",
        "notes",
    ]


# API views. Maybe delete.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["encampment"]
    ordering = "date"


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class EncampmentViewSet(viewsets.ModelViewSet):
    queryset = Encampment.objects.all()
    serializer_class = EncampmentSerializer
