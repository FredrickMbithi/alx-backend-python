from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    user.delete()  # This triggers post_delete signals
    return redirect('home')  # or any page after deletion
