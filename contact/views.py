from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from contact.forms import MessageForm
from django.utils.translation import gettext as _

# Create your views here.


def sentMessage(request):
    if request.method == "POST":
        m = MessageForm(request.POST)
        if m.is_valid():
            if request.user.is_authenticated:
                m.instance.user = request.user
            m.save()

            # Send email confirmation
            subject = _("Thank you for contacting us")
            message = _(
                "Dear {name}, Thanks for contacting us! "
                "We have received your message: {message} "
                "and will get back to you as soon as possible."
            ).format(name=m.cleaned_data["name"], message=m.cleaned_data["message"])
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [m.cleaned_data["email"]]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(
                request,
                _(
                    "Thanks for contacting us. Your message has been submitted successfully, and a confirmation email has been sent."
                ),
            )
            return HttpResponseRedirect(request.path_info)
    else:
        if request.user.is_authenticated:
            m = MessageForm(
                initial={"name": request.user.first_name, "email": request.user.email}
            )
        else:
            m = MessageForm()

    return render(request, "contact/contact.html", {"m": m})
