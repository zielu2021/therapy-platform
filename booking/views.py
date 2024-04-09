from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from home.models import PDFFile
from .models import *


@login_required
def index(request):
    return render(request, "booking/index.html", {})


@login_required
def booking(request):
    # Calling 'validWeekday' Function to Loop open days in the next 21 days
    weekdays = validWeekday(22)
    # If now is later then last TIME_CHOICES do not show this day
    current_hour = datetime.now().hour
    time_choices = [hour for hour, _ in TIME_CHOICES]
    # Convert the last item from time_choices to 24-hour format
    last_item = time_choices[-1]
    last_hour = int(last_item[:-2])  # Extract the hour part
    if "PM" in last_item.upper() and last_hour != 12:  # Convert to 24-hour format if PM
        last_hour += 12

    if int(current_hour) >= int(last_hour):
        weekdays.pop(0)  # Remove today from select day option after closing

    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == "POST":
        service = request.POST.get("service")
        day = request.POST.get("day")
        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect("booking")

        # Store day and service in django session:
        request.session["day"] = day
        request.session["service"] = service

        return redirect("bookingSubmit")

    return render(
        request,
        "booking/booking.html",
        {
            "weekdays": weekdays,
            "validateWeekdays": validateWeekdays,
        },
    )


@login_required
def bookingSubmit(request):
    user = request.user
    today = timezone.now()
    min_date = today.strftime("%Y-%m-%d")
    max_date = (today + timedelta(days=21)).strftime("%Y-%m-%d")

    day = request.session.get("day")
    service = request.session.get("service")

    # comparing hours from time choices to actuall time(hour)- not showing today's past hours
    current_hour_12h = datetime.now().strftime("%I %p")
    times_today = [
        hour
        for hour, _ in TIME_CHOICES
        if datetime.strptime(hour, "%I %p")
        > datetime.strptime(current_hour_12h, "%I %p")
        and not Appointment.objects.filter(day=day, time=hour).exists()
    ]
    times_future = [
        hour
        for hour, _ in TIME_CHOICES
        if not Appointment.objects.filter(day=day, time=hour).exists()
    ]

    times = times_today if day == timezone.now().strftime("%Y-%m-%d") else times_future

    if request.method == "POST":
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if (
            service
            and min_date <= day <= max_date
            and date
            in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
        ):
            if Appointment.objects.filter(day=day).count() < len(times):
                if not Appointment.objects.filter(day=day, time=time).exists():
                    Appointment.objects.get_or_create(
                        user=user,
                        service=service,
                        day=day,
                        time=time,
                    )

                    # sending email after saved appointment
                    messages.success(
                        request,
                        _("Appointment Saved! Check your email with confirmation."),
                    )

                    subject = _("Appointment Confirmation")
                    message = _(
                        "Your appointment for %(service)s on %(day)s at %(time)s has been confirmed."
                    ) % {"service": service, "day": day, "time": time}
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [user.email]
                    send_mail(subject, message, from_email, recipient_list)

                    # removing day and service session
                    request.session.pop("day", None)
                    request.session.pop("service", None)

                    return redirect("bookingIndex")
                else:
                    messages.success(
                        request, "The Selected Time Has Been Reserved Before!"
                    )
            else:
                messages.success(request, "The Selected Day Is Full!")
        else:
            messages.success(request, "Invalid Selection!")

    return render(
        request,
        "booking/bookingSubmit.html",
        {
            "times": times,
        },
    )


@login_required
def userPanel(request):
    user = request.user
    # access for authenticated user to files for download
    pdf_files = PDFFile.objects.all()
    appointments = Appointment.objects.filter(user=user).order_by("-day", "-time")
    return render(
        request,
        "booking/userPanel.html",
        {
            "user": user,
            "appointments": appointments,
            "pdf_files": pdf_files,
        },
    )


@login_required
def userUpdate(request, id):
    # taking appointment to edit and converting date and time to compare with actuall time- and check 24h difference
    appointment = get_object_or_404(Appointment, pk=id)
    appointment_datetime_str = f"{appointment.day} {appointment.time.upper()}"
    appointment_datetime = timezone.make_aware(
        datetime.strptime(appointment_datetime_str, "%Y-%m-%d %I %p")
    )
    now = timezone.now()
    time_difference = appointment_datetime - now
    if time_difference > timedelta(hours=24):
        appointment = Appointment.objects.get(pk=id)
        weekdays = validWeekday(22)
        validateWeekdays = isWeekdayValid(weekdays)
        if request.method == "POST":
            service = request.POST.get("service")
            day = request.POST.get("day")

            # Store day and service in django session:
            request.session["day"] = day
            request.session["service"] = service

            return redirect("userUpdateSubmit", id=id)

        return render(
            request,
            "booking/userUpdate.html",
            {
                "weekdays": weekdays,
                "validateWeekdays": validateWeekdays,
                "id": id,
            },
        )

    else:
        messages.success(request, "You can't edit less then 24h before!")
        return redirect("userPanel")


@login_required
def userUpdateSubmit(request, id):
    user = request.user
    today = timezone.now()
    min_date = today.strftime("%Y-%m-%d")
    max_date = (today + timedelta(days=21)).strftime("%Y-%m-%d")

    day = request.session.get("day")
    service = request.session.get("service")

    # Only show the time of the day that has not been selected before and the time that is editing:
    current_hour_12h = datetime.now().strftime("%I %p")
    times_today = [
        hour
        for hour, _ in TIME_CHOICES
        if datetime.strptime(hour, "%I %p")
        > datetime.strptime(current_hour_12h, "%I %p")
        and not Appointment.objects.filter(day=day, time=hour).exists()
    ]
    # times_today = [hour for hour in TIME_CHOICES if datetime.strptime(hour, '%I %p') > today and checkEditTime([hour], day, id)]
    times_future = [
        hour
        for hour, _ in TIME_CHOICES
        if not Appointment.objects.filter(day=day, time=hour).exists()
    ]

    if day == today.strftime("%Y-%m-%d"):
        times = times_today
    else:
        times = times_future

    appointment = Appointment.objects.get(pk=id)
    user_selected_time = appointment.time

    if request.method == "POST":
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if (
            service
            and min_date <= day <= max_date
            and date
            in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
        ):
            if times and (
                Appointment.objects.filter(day=day, time=time).count() < 1
                or user_selected_time == time
            ):
                Appointment.objects.filter(pk=id).update(
                    user=user,
                    service=service,
                    day=day,
                    time=time,
                )
                messages.success(
                    request,
                    _(
                        "Appointment Edited! Check your email with new date confirmation"
                    ),
                )

                # Send email to the user about successful changed
                subject = _("Appointment Edited Successfully")
                message = _(
                    "Your edited appointment for %(service)s on %(day)s at %(time)s has been confirmed."
                ) % {"service": service, "day": day, "time": time}
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)

                # Remove session variables after using them
                request.session.pop("day", None)
                request.session.pop("service", None)

                return redirect("bookingIndex")
            else:
                messages.success(
                    request,
                    "The Selected Time Has Been Reserved Before or is not available!",
                )
        else:
            messages.success(request, "Invalid Selection!")

    return render(
        request,
        "booking/userUpdateSubmit.html",
        {
            "times": times,
            "id": id,
        },
    )


@login_required
# to access staff panel user must be staff
@user_passes_test(lambda user: user.is_staff, login_url="home")
def staffPanel(request):
    today = timezone.now()
    minDate = today.strftime("%Y-%m-%d")
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime("%Y-%m-%d")
    maxDate = strdeltatime
    # Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by(
        "day", "time"
    )

    return render(
        request,
        "booking/staffPanel.html",
        {
            "items": items,
        },
    )


def dayToWeekday(x):
    z = timezone.make_aware(datetime.strptime(x, "%Y-%m-%d"))
    y = z.strftime("%A")
    return y


def validWeekday(days):
    # Loop through the chosen number of days ahead:
    today = timezone.now()
    weekdays = []
    for i in range(0, days):
        x = today + timedelta(days=i)
        y = x.strftime("%A")
        if (
            y == "Monday"
            or y == "Tuesday"
            or y == "Wednesday"
            or y == "Thursday"
            or y == "Friday"
            or y == "Saturday"
        ):
            weekdays.append(x.strftime("%Y-%m-%d"))
    # return days of week in chosen period that are open-hours
    return weekdays


def isWeekdayValid(valid_weekdays):
    # checking if some of working day is not full
    validateWeekdays = []
    # return list on hours to choose, compare to quantity of actual booked appointments
    time_choices = [hour for hour, _ in TIME_CHOICES]
    for j in valid_weekdays:
        if Appointment.objects.filter(day=j).count() < len(time_choices):
            validateWeekdays.append(j)
    return validateWeekdays


def checkTime(times, day):
    # Only show the time of the day that has not been selected before (each hour choice can has 1 appointment):
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x


def checkEditTime(times, day, id):
    # Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
