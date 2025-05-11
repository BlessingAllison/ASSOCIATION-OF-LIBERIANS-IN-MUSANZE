from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse, NoReverseMatch
from django.shortcuts import redirect
from django.contrib import messages


class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?
        
        # Define paths that don't require authentication
        public_paths = [
            reverse('account_login'),
            reverse('account_register'),
            '/admin/',
            '/static/',
            '/media/'
        ]
        
        # Skip middleware for public paths
        if any(request.path.startswith(path) for path in public_paths):
            return None
            
        if user.is_authenticated:
            try:
                if user.user_type == '1':  # Admin
                    if modulename == 'voting.views':
                        try:
                            if request.path != reverse('voting:fetch_ballot'):
                                messages.error(
                                    request, "You do not have access to this resource")
                                return redirect(reverse('adminDashboard'))
                        except NoReverseMatch:
                            pass  # Skip if URL can't be reversed
                elif user.user_type == '2':  # Voter
                    if modulename == 'administrator.views':
                        messages.error(
                            request, "You do not have access to this resource")
                        return redirect(reverse('voting:voterDashboard'))
                else:  # None of the aforementioned ? Please take the user to login page
                    return redirect(reverse('account_login'))
            except Exception as e:
                # Log the error and allow the request to continue
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error in middleware: {str(e)}")
        else:
            # If the path is login or has anything to do with authentication, pass
            try:
                if request.path == reverse('account_login') or request.path == reverse('account_register') or modulename == 'django.contrib.auth.views':
                    return None
            except NoReverseMatch:
                pass
                
            # If we get here, the user is not authenticated and not on a public path
            return redirect(reverse('account_login'))
            
        return None
