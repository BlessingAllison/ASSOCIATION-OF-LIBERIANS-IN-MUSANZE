from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse, NoReverseMatch, resolve
from django.shortcuts import redirect
from django.contrib import messages


class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware for static and media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None
            
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?
        
        # Define paths that don't require authentication
        public_paths = [
            '/account/login',
            '/account/register',
            '/admin',
            '/static',
            '/media',
            '/account/logout'
        ]
        
        # Normalize the path by removing trailing slash for comparison
        normalized_path = request.path.rstrip('/')
        
        # Check if the current path is a public path
        is_public_path = any(normalized_path.startswith(path.rstrip('/')) for path in public_paths)
        
        # Skip middleware for public paths and root URL
        if is_public_path or normalized_path == '':
            return None
            
        # Handle authenticated users
        if user.is_authenticated:
            try:
                if user.user_type == '1':  # Admin
                    if modulename == 'voting.views' and request.path != reverse('voting:fetch_ballot'):
                        messages.error(
                            request, "You do not have access to this resource")
                        return redirect('administrator:adminDashboard')
                elif user.user_type == '2':  # Voter
                    if modulename == 'administrator.views':
                        messages.error(
                            request, "You do not have access to this resource")
                        return redirect('voting:voterDashboard')
                else:  # None of the aforementioned ? Please take the user to login page
                    return redirect('account:login')
            except NoReverseMatch as e:
                # Log the error and allow the request to continue
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"URL reversal error in middleware: {str(e)}")
                return None
        else:
            # If we get here, the user is not authenticated and not on a public path
            # Redirect to login with the 'next' parameter
            login_url = reverse('account:login')
            if normalized_path != login_url.rstrip('/'):
                return redirect(f"{login_url}?next={request.path}")
            return None
