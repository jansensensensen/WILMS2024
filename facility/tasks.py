# tasks.py (inside your app directory)

from celery import shared_task
from .views import apply_promo_and_main_rules  # Import your function

@shared_task
def execute_rules():
    apply_promo_and_main_rules(None)  # Pass a placeholder request or adjust accordingly
