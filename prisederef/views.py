from django.db.models import Count
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Candidate, Reference, Referent, Corporation, ReferenceInteraction


@login_required
def recruiter_home(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        candidate_name = request.POST.get("candidate_name", "").strip()
        if candidate_name:
            Candidate.objects.create(name=candidate_name)
            return redirect("candidates")
    
    candidates = (
        Candidate.objects.annotate(num_refs=Count("references"))
        .order_by("name")
    )
    
    return render(
        request,
        "recruiter_home.html",
        {
            "candidates": candidates,
        },
    )


def invite_landing(request: HttpRequest, token) -> HttpResponse:
    candidate = get_object_or_404(Candidate, invite_token=token)
    submitted = Reference.objects.filter(candidate=candidate).count()
    if submitted >= 3:
        return render(request, "invite_closed.html", {"candidate": candidate})
    return render(request, "invite_form.html", {"candidate": candidate})


def submit_reference(request: HttpRequest, token) -> HttpResponse:
    candidate = get_object_or_404(Candidate, invite_token=token)
    if request.method != "POST":
        return redirect("invite_landing", token=token)

    submitted = Reference.objects.filter(candidate=candidate).count()
    if submitted >= 3:
        return render(request, "invite_closed.html", {"candidate": candidate})

    # Debug: Print all POST data
    print(f"DEBUG: POST data received: {dict(request.POST)}")
    
    # Process up to 3 references
    references_created = 0
    errors = []

    for i in range(1, 4):  # Process references 1, 2, and 3
        referent_name = request.POST.get(f"referent_name_{i}", "").strip()
        referent_email = request.POST.get(f"referent_email_{i}", "").strip()
        referent_phone = request.POST.get(f"referent_phone_{i}", "").strip()
        referent_role = request.POST.get(f"referent_role_{i}", "").strip()
        corporation_name = request.POST.get(f"corporation_name_{i}", "").strip()
        comment = request.POST.get(f"comment_{i}", "").strip()

        print(f"DEBUG: Processing reference {i}: name='{referent_name}', email='{referent_email}', phone='{referent_phone}', corp='{corporation_name}'")

        # Skip empty references
        if not referent_name and not referent_email and not referent_phone and not corporation_name:
            print(f"DEBUG: Skipping empty reference {i}")
            continue

        # Validate required fields for this reference
        if not referent_name:
            errors.append(f"Référence {i}: Nom du référent requis.")
            continue
        if not referent_email:
            errors.append(f"Référence {i}: Email du référent requis.")
            continue
        if not referent_phone:
            errors.append(f"Référence {i}: Téléphone du référent requis.")
            continue
        if not corporation_name:
            errors.append(f"Référence {i}: Entreprise requise.")
            continue

        # Create the reference
        try:
            corporation, _ = Corporation.objects.get_or_create(name=corporation_name)
            referent = Referent.objects.create(
                name=referent_name,
                role=referent_role,
                email=referent_email,
                phone=referent_phone,
            )

            Reference.objects.create(
                candidate=candidate,
                corporation=corporation,
                referent=referent,
                comment=comment,
            )
            references_created += 1
        except Exception as e:
            errors.append(f"Référence {i}: Erreur lors de la création - {str(e)}")

    # If there are validation errors, show them
    if errors:
        return render(
            request,
            "invite_form.html",
            {"candidate": candidate, "error": " ".join(errors)},
        )

    # If no references were created, show error
    if references_created == 0:
        print("DEBUG: No references were created")
        return render(
            request,
            "invite_form.html",
            {"candidate": candidate, "error": "Au moins une référence complète est requise."},
        )
    
    print(f"DEBUG: Successfully created {references_created} references")

    return render(
        request,
        "invite_thanks.html",
        {"candidate": candidate},
    )


@login_required
def references_view(request: HttpRequest) -> HttpResponse:
    # Filters / search
    q = request.GET.get("q", "").strip()

    references_qs = (
        Reference.objects.select_related("candidate", "corporation", "referent")
        .prefetch_related("interactions")
        .order_by("-created_at")
    )

    if q:
        from django.db.models import Q

        references_qs = references_qs.filter(
            Q(candidate__name__icontains=q)
            | Q(referent__name__icontains=q)
            | Q(corporation__name__icontains=q)
            | Q(referent__email__icontains=q)
            | Q(referent__phone__icontains=q)
        )

    return render(
        request,
        "references.html",
        {
            "references": references_qs,
            "q": q,
        },
    )


@login_required
def reference_detail_view(request: HttpRequest, reference_id: int) -> HttpResponse:
    """View individual reference details with interactions"""
    try:
        reference = Reference.objects.select_related(
            'candidate', 'corporation', 'referent'
        ).prefetch_related('interactions').get(id=reference_id)
    except Reference.DoesNotExist:
        messages.error(request, "Référence introuvable.")
        return redirect("references")
    
    # Handle interaction logging
    if request.method == "POST":
        interaction_type = request.POST.get("interaction_type")
        comment = request.POST.get("comment", "").strip()
        feedback = request.POST.get("feedback", "").strip() or None
        
        if interaction_type:
            ReferenceInteraction.objects.create(
                reference=reference,
                recruiter=request.user,
                interaction_type=interaction_type,
                comment=comment,
                feedback=feedback
            )
            messages.success(request, "Interaction enregistrée avec succès.")
            return redirect("reference_detail", reference_id=reference_id)
        else:
            messages.error(request, "Veuillez sélectionner un type d'interaction.")
    
    return render(request, "reference_detail.html", {
        "reference": reference
    })
