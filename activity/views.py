from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, WeeklyReport


# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        staff_no = request.POST.get("staff_no")
        password = request.POST.get("password")

        employee = Employee.objects.filter(
            staff_no=staff_no,
            password=password
        ).first()

        if employee:
            request.session["employee_id"] = employee.id
            request.session["role"] = employee.role

            if employee.role == "Employee":
                return redirect("dashboard")
            elif employee.role == "Group Head":
                return redirect("gh_dashboard")
            elif employee.role == "HR":
                return redirect("hr_dashboard")

        return render(request, "login.html", {"error": "Invalid Credentials"})

    return render(request, "login.html")


# ================= EMPLOYEE DASHBOARD (SUBMIT PAGE) =================
def dashboard_view(request):
    employee_id = request.session.get("employee_id")
    role = request.session.get("role")

    if not employee_id or role != "Employee":
        return redirect("login")

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        WeeklyReport.objects.create(
            employee=employee,
            date=request.POST.get("date"),
            current_week_activity=request.POST.get("current_week_activity"),
            next_week_activity=request.POST.get("next_week_activity"),
            leave_taken=request.POST.get("leave_taken"),
            remarks=request.POST.get("remarks"),
            gh_status="Pending",
            hr_status="Pending",
        )
        return redirect("my_reports")

    return render(request, "dashboard.html", {
        "employee": employee
    })


# ================= MY REPORTS =================
def my_reports(request):
    employee_id = request.session.get("employee_id")
    role = request.session.get("role")

    if not employee_id or role != "Employee":
        return redirect("login")

    employee = get_object_or_404(Employee, id=employee_id)

    reports = WeeklyReport.objects.filter(
        employee=employee
    ).order_by("-created_at")

    return render(request, "my_reports.html", {
        "reports": reports
    })


# ================= REPORT DETAIL =================
def report_detail(request, id):
    employee_id = request.session.get("employee_id")
    role = request.session.get("role")

    if not employee_id or role != "Employee":
        return redirect("login")

    report = get_object_or_404(
        WeeklyReport,
        id=id,
        employee_id=employee_id
    )

    return render(request, "report_detail.html", {
        "report": report
    })


# == gh
# ================= GH DASHBOARD =================
def gh_dashboard(request):
    if request.session.get("role") != "Group Head":
        return redirect("login")

    employee_id = request.session.get("employee_id")
    employee = get_object_or_404(Employee, id=employee_id)

    reports = WeeklyReport.objects.all().order_by("-created_at")

    return render(request, "gh_dashboard.html", {
        "reports": reports,
        "employee": employee
    })


# ================= GH APPROVE =================
def gh_approve(request, id):
    if request.session.get("role") != "Group Head":
        return redirect("login")

    if request.method == "POST":
        report = get_object_or_404(WeeklyReport, id=id)
        report.gh_status = "Approved"
        report.save()

    return redirect("gh_dashboard")


# ================= GH REJECT =================
def gh_reject(request, id):
    if request.session.get("role") != "Group Head":
        return redirect("login")

    if request.method == "POST":
        report = get_object_or_404(WeeklyReport, id=id)
        report.gh_status = "Rejected"
        report.hr_status = "Rejected"  # Final rejection
        report.save()

    return redirect("gh_dashboard")
    
# ================= HR DASHBOARD (FINAL APPROVAL) =================
def hr_dashboard(request):
    if request.session.get("role") != "HR":
        return redirect("login")

    reports = WeeklyReport.objects.filter(
        gh_status="Approved"
    ).order_by("-created_at")

    return render(request, "hr_dashboard.html", {
        "reports": reports
    })


def hr_approve(request, id):
    if request.session.get("role") != "HR":
        return redirect("login")

    report = get_object_or_404(WeeklyReport, id=id)

    if report.gh_status == "Approved":
        report.hr_status = "Approved"
        report.save()

    return redirect("hr_dashboard")


def hr_reject(request, id):
    if request.session.get("role") != "HR":
        return redirect("login")

    report = get_object_or_404(WeeklyReport, id=id)

    report.hr_status = "Rejected"
    report.save()

    return redirect("hr_dashboard")


# ================= LOGOUT =================
def logout_view(request):
    request.session.flush()
    return redirect("login")