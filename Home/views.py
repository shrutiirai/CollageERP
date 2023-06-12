from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Student, Staff, BookIssue, Library, Enrollment, Attendance
from .models import Course as CourseModel

def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Student').exists():
            # Authenticated student logic here
            students = Student.objects.filter(user=request.user)
            courses = students.first().courses.all()
            enrollment_counts = [student.enrollment_set.count() for student in students]
            context = {
                'students': students,
                'enrollment_counts': enrollment_counts,
                'courses': courses
            }
            return render(request, 'index.html', context)
        elif request.user.groups.filter(name='Teacher').exists():
            # Authenticated staff logic here
            staffs = Staff.objects.filter(user=request.user)
            context = {
                'staffs': staffs,
            }
            return render(request, 'index.html', context)
        else:
            # User doesn't belong to either group, handle as needed
            return HttpResponse('Unauthorized access')
    else:
        # Unauthenticated user logic here
        return redirect('login')


@login_required
def attendance(request):
    # Check if the authenticated user is a staff member
    is_staff = request.user.groups.filter(name='Teacher').exists()

    if is_staff:
        # Staff can update and see attendance of all students
        if request.method == 'POST':
            is_present = request.POST.get('is_present')
            enrollment_id = request.POST.get('enrollment_id')
            enrollment = Enrollment.objects.get(id=enrollment_id)

            attendance = Attendance.objects.create(enrollment=enrollment, is_present=is_present)

            return redirect('attendance')
        else:
            staffs = Staff.objects.filter(user=request.user)
            enrollments = Enrollment.objects.all()
            context = {
                'enrollments': enrollments,
                'staffs': staffs
            }
            return render(request, 'Attendance.html', context)
    else:
        # Students can only see their own attendance
        student = Student.objects.get(user=request.user)
        enrollments = Enrollment.objects.filter(student=student)
        context = {
            'enrollments': enrollments
        }
        return render(request, 'Attendance.html', context)

def Course(request):
    if request.user.groups.filter(name='Teacher').exists():
        # Authenticated staff logic here
        staffs = Staff.objects.filter(user=request.user)
        courses = CourseModel.objects.all()
        # courses = Course.objects.all()
        # students = Student.objects.filter(user=request.user)
        enrolled_students = Enrollment.objects.select_related('student').filter(course__in=courses)
        context = {
            'staffs': staffs,
            'courses': courses,
            'enrolled_students': enrolled_students,
        }
        return render(request, 'Course.html', context)
    else:
        # User doesn't belong to the 'Teacher' group, handle as needed
        return HttpResponse('Unauthorized access')


# def Enrollment(request):
#     return render(request, 'Enrollment.html')


def Finance(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Student').exists():
            return redirect('view_fees')
        elif request.user.groups.filter(name='Teacher').exists():
            return redirect('update_fees', student_id=student_id)


def view_fees(request):
    student = request.user.student
    finance = get_object_or_404(Finance, enrollment__student=student)
    return render(request, 'Finance.html', {'finance': finance})


def update_fees(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    finance = get_object_or_404(Finance, enrollment__student=student)

    if request.method == 'POST':
        form = FinanceForm(request.POST, instance=finance)
        if form.is_valid():
            form.save()
            return redirect('view_fees')
    else:
        form = FinanceForm(instance=finance)

    return render(request, 'Finance.html', {'student': student, 'form': form})


@login_required
def library_view(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Student').exists():
            # Authenticated student logic here
            student = Student.objects.get(user=request.user)
            issued_books = BookIssue.objects.filter(enrollment__student=student)
            current_date = date.today()
            available_books = Library.objects.filter(book_quantity__gt=0)
            context = {
                'students': [student],  # Pass student as a single-item list
                'issued_books': issued_books,
                'current_date': current_date,
                'available_books': available_books
            }
            return render(request, 'Library.html', context)
        elif request.user.groups.filter(name='Teacher').exists():
            # Authenticated staff logic here
            if request.method == 'POST':
                action = request.POST.get('action')
                book_id = request.POST.get('book_id')
                student_id = request.POST.get('student_id')

                if action == 'allocate':
                    book = Library.objects.get(id=book_id)
                    student = Student.objects.get(id=student_id)
                    BookIssue.objects.create(enrollment=student.enrollment_set.first(), book=book, due_date=date.today())
                    return redirect('library')

                elif action == 'deallocate':
                    book_issue_id = request.POST.get('book_issue_id')
                    book_issue = BookIssue.objects.get(id=book_issue_id)
                    book_issue.delete()
                    return redirect('library')

            staffs = Staff.objects.filter(user=request.user)
            students = Student.objects.all()
            issued_books = BookIssue.objects.all()
            available_books = Library.objects.filter(book_quantity__gt=0)
            context = {
                'staffs': staffs,
                'student': students,
                'issued_books': issued_books,
                'available_books': available_books
            }
            return render(request, 'Library.html', context)

    # Return a default response if user is not authenticated or doesn't belong to any group
    return HttpResponse("Access denied.")


def Placement(request):
    return render(request, 'Placement.html')


@login_required
def student(request):
    if request.user.groups.filter(name='Teacher').exists():
        # Authenticated staff logic here
        students = Student.objects.all()
        courses = CourseModel.objects.all()
        # courses = students.first().courses.all()
        staffs = Staff.objects.filter(user=request.user)
        context = {
            'student': students,
            'staffs': staffs,
            'courses': courses,
        }
        return render(request, 'Student.html', context)
    else:
        # User doesn't belong to the 'Teacher' group, handle as needed
        return HttpResponse('Unauthorized access')


def user_login(request):
    if request.method == "POST":
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            return redirect('HOME')  # Redirect to the 'HOME' page after successful login
        else:
            error_message = "Invalid Credentials, Please try again"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def user_logout(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect('login')
