# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from userservice.user import UserService


@method_decorator(login_required, name='dispatch')
class PageView(TemplateView):
    """
    PageView renders the 'index.html' template and provides user context.

    This view extends Django's TemplateView and injects two user-related
    context variables:
    - 'user_netid': The NetID of the actually authenticated user,
                    retrieved via UserService.get_original_user().
    - 'user_override': The current user (possibly overridden),
                        retrieved via UserService.get_user().

    Returns:
        dict: Context data including user information for template rendering.
    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        us = UserService()
        context['user_netid'] = us.get_original_user()
        context['user_override'] = us.get_user()
        return context


class DefaultPageView(PageView):
    template_name = "index.html"
