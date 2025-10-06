from django.contrib import admin

from .models import Candidate, Corporation, Referent, Reference


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")




@admin.register(Corporation)
class CorporationAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")


@admin.register(Referent)
class ReferentAdmin(admin.ModelAdmin):
    search_fields = ("name", "email", "phone", "role")
    list_display = ("id", "name", "role", "email", "phone")


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    autocomplete_fields = ("recruiter", "candidate", "corporation", "referent")
    list_display = (
        "id",
        "recruiter",
        "interview_date",
        "candidate",
        "corporation",
        "referent",
    )
    list_filter = ("recruiter", "corporation", "interview_date")
    search_fields = (
        "comment",
        "recruiter__name",
        "candidate__name",
        "corporation__name",
        "referent__name",
        "referent__email",
        "referent__phone",
    )
