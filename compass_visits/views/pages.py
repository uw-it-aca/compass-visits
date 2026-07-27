# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from persistent_message.models import Message
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

        context['messages'] = []

        message_level_hierarchy = ['info', 'success', 'warning', 'danger']
        highest_level = None

        for message in Message.objects.active_messages():
            if message.get_level_display().lower() in message_level_hierarchy:
                if (highest_level is None
                    or message_level_hierarchy.index(
                        message.get_level_display().lower()) >
                        message_level_hierarchy.index(highest_level)):
                    highest_level = message.get_level_display().lower()
            context['messages'].append(message.render())

        context['message_level'] = highest_level or "info"
        return context


class DefaultPageView(PageView):
    template_name = "index.html"
