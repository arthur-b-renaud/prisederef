from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Candidate(models.Model):
    name = models.CharField(max_length=200)
    invite_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self) -> str:
        return self.name




class Corporation(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class Referent(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.name


class Reference(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="references",
        null=True,
        blank=True,
    )
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name="references")
    corporation = models.ForeignKey(Corporation, on_delete=models.PROTECT, related_name="references")
    referent = models.ForeignKey(Referent, on_delete=models.PROTECT, related_name="references")
    interview_date = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-interview_date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.candidate} @ {self.corporation} with {self.referent}"


class ReferenceInteraction(models.Model):
    INTERACTION_TYPES = [
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('meeting', 'Réunion'),
        ('other', 'Autre'),
    ]
    
    FEEDBACK_CHOICES = [
        ('positive', 'Positif'),
        ('neutral', 'Neutre'),
        ('negative', 'Négatif'),
    ]

    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name="interactions")
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reference_interactions")
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    interaction_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    feedback = models.CharField(max_length=10, choices=FEEDBACK_CHOICES, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-interaction_date"]

    def __str__(self) -> str:
        return f"{self.get_interaction_type_display()} - {self.reference.candidate.name} ({self.get_feedback_display() if self.feedback else 'Pas de feedback'})"
