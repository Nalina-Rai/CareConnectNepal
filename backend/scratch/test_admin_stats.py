import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careconnect.settings')
django.setup()

from users.models import User, KYCDocument
from jobs.models import Job, Application
from support.models import Ticket
from django.utils import timezone
from datetime import timedelta

try:
    print("Starting query...")
    total_users = User.objects.filter(role=User.Roles.USER).count()
    total_ngos = User.objects.filter(role=User.Roles.NGO).count()
    active_jobs = Job.objects.filter(status__in=[Job.Status.OPEN, Job.Status.ACTIVE]).count()
    pending_kyc = KYCDocument.objects.filter(status=KYCDocument.Status.PENDING).count()
    total_applications = Application.objects.count()

    print("Counts:", total_users, total_ngos, active_jobs, pending_kyc, total_applications)

    # Registration stats for last 6 months
    now = timezone.now()
    monthly_registrations = []
    for i in range(5, -1, -1):
        month_start = (now - timedelta(days=30 * i)).replace(day=1, hour=0, minute=0, second=0)
        if i > 0:
            month_end = (now - timedelta(days=30 * (i - 1))).replace(day=1, hour=0, minute=0, second=0)
        else:
            month_end = now
        count = User.objects.filter(date_joined__gte=month_start, date_joined__lt=month_end).count()
        monthly_registrations.append({
            "month": month_start.strftime("%b %Y"),
            "count": count,
        })
    print("Monthly registrations:", monthly_registrations)

    recent_kyc = list(KYCDocument.objects.filter(reviewed_at__isnull=False).select_related("user").order_by("-reviewed_at")[:50])
    recent_jobs = list(Job.objects.order_by("-updated_at")[:50])
    recent_users = list(User.objects.order_by("-date_joined")[:50])
    recent_tickets = list(Ticket.objects.order_by("-updated_at")[:50])

    print("Fetched lists successfully. kyc:", len(recent_kyc), "jobs:", len(recent_jobs), "users:", len(recent_users), "tickets:", len(recent_tickets))

    recent_activity = []

    for kyc in recent_kyc:
        user_name = kyc.user.full_name or kyc.user.username or kyc.user.email or f"User {kyc.user_id}"
        if kyc.status == KYCDocument.Status.VERIFIED:
            title = "KYC approved"
            desc = f"{user_name} was verified by admin."
            activity_type = "kyc_approved"
        elif kyc.status == KYCDocument.Status.REJECTED:
            title = "KYC rejected"
            desc = f"{user_name}'s verification was rejected."
            activity_type = "kyc_rejected"
        elif kyc.status == KYCDocument.Status.INFO_REQUESTED:
            title = "KYC info requested"
            desc = f"More information was requested from {user_name}."
            activity_type = "kyc_info_requested"
        else:
            continue

        recent_activity.append({
            "id": f"kyc-{kyc.id}",
            "type": activity_type,
            "title": title,
            "desc": desc,
            "timestamp": kyc.reviewed_at.isoformat(),
        })

    for job in recent_jobs:
        if job.created_at == job.updated_at:
            title = "Job posted"
            activity_type = "job_posted"
            desc = f"New job '{job.title}' was added."
            timestamp = job.created_at
        else:
            title = "Job updated"
            activity_type = "job_updated"
            status_label = job.get_status_display()
            desc = f"Job '{job.title}' was updated (status: {status_label})."
            timestamp = job.updated_at

        recent_activity.append({
            "id": f"job-{job.id}-{int(timestamp.timestamp())}",
            "type": activity_type,
            "title": title,
            "desc": desc,
            "timestamp": timestamp.isoformat(),
        })

    for user in recent_users:
        recent_activity.append({
            "id": f"user-{user.id}",
            "type": "user_registered",
            "title": "User registered",
            "desc": f"{user.full_name or user.username} joined the platform.",
            "timestamp": user.date_joined.isoformat(),
        })

    for ticket in recent_tickets:
        user_name = ticket.user.full_name or ticket.user.username or "Anonymous"
        if ticket.status == Ticket.Status.RESOLVED:
            title = "Issue resolved"
            desc = f"Support ticket '{ticket.subject}' from {user_name} was marked as resolved."
            activity_type = "ticket_resolved"
        elif ticket.created_at == ticket.updated_at:
            title = "New issue reported"
            desc = f"{user_name} submitted a new support ticket: '{ticket.subject}'"
            activity_type = "ticket_created"
        else:
            continue

        recent_activity.append({
            "id": f"ticket-{ticket.id}",
            "type": activity_type,
            "title": title,
            "desc": desc,
            "timestamp": ticket.updated_at.isoformat(),
        })

    recent_activity = sorted(recent_activity, key=lambda item: item["timestamp"], reverse=True)[:7]
    print("Success! Number of activities:", len(recent_activity))

except Exception as e:
    print("ERROR OCCURRED:")
    traceback.print_exc()
