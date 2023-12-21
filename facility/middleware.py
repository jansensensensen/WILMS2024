from .views import apply_promo_and_main_rules, user_apply_promo_and_main_rules

class ApplyRulesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Call your function to apply rules
        apply_promo_and_main_rules(request)
        user_apply_promo_and_main_rules(request)
        
        response = self.get_response(request)
        return response
    

