from django.contrib import admin
from .models import Course, Student, Enrollment, Attendance, Library, BookIssue, Finance, Placement, Staff

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'department')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'dob')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'is_present')

# class ExamAdmin(admin.ModelAdmin):
#     list_display = ('enrollment', 'date', 'subject', 'marks')

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'book_author', 'book_publisher', 'book_quantity')

class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'book', 'issue_date', 'due_date')

class FinanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'total_fee', 'paid_fee', 'remaining_fee')

class PlacementAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'company_name', 'job_title', 'salary', 'date_of_placement')


admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
# admin.site.register(Exam, ExamAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(BookIssue, BookIssueAdmin)
admin.site.register(Finance, FinanceAdmin)
admin.site.register(Placement, PlacementAdmin)
admin.site.register(Staff, StaffAdmin)
