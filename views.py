# pylint: disable=no-member, line-too-long

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, password_validation
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

@staff_member_required
def simple_dashboard_home(request):
    context = {}

    return render(request, 'simple_dashboard_home.html', context=context)

@staff_member_required
def simple_dashboard_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('simple_dashboard_home'))

@staff_member_required
def simple_dashboard_account(request):
    context = {}

    context['password_requirements'] = password_validation.password_validators_help_texts()

    context['messages'] = []

    if request.method == 'POST':
        email = request.POST.get('email', '')

        if email != request.user.email:
            request.user.email = email

            request.user.save()

            context['messages'].append('E-mail address updated successfully.')

        current_password = request.POST.get('current-password', None)
        new_password = request.POST.get('new-password', None)

        if new_password != '': # nosec
            if request.user.check_password(current_password) is True:
                try:
                    password_validation.validate_password(new_password, user=request.user)
                    request.user.set_password(new_password)
                    request.user.save()
                    context['messages'].append('Password updated successfully.')
                except ValidationError as error:
                    for validation_error in error.messages:
                        context['messages'].append('Unable to update password: ' + str(validation_error))
            else:
                context['messages'].append('Unable to update password, invalid current password provided.')

    context['user'] = request.user

    return render(request, 'simple_dashboard_account.html', context=context)

def simple_dashboard_favicon(request):
    context = {
        'fill_value': '#610FED'
    }

    return render(request, 'dashboard/simple_dashboard_favicon.svg', context=context, content_type='image/svg+xml')

