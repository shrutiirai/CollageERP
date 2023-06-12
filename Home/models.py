from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, Group


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField()
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=6, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    courses = models.ManyToManyField('Home.Course', through='Home.Enrollment')
    groups = models.ManyToManyField(Group, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def enrollment_count(self):
        return self.enrollment_set.count()

    def get_courses(self):
        return self.courses.all()

    def get_attendance(self):
        enrollments = self.enrollment_set.all()
        attendance = Attendance.objects.filter(enrollment__in=enrollments)
        return attendance


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=6, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=255)
    image = models.ImageField(upload_to='staff_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    student = models.ForeignKey('Home.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Home.Course', on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}"

    def get_attendance(self):
        return Attendance.objects.filter(enrollment=self)


class Attendance(models.Model):
    enrollment = models.ForeignKey('Home.Enrollment', on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField()

    def __str__(self):
        return f"{self.enrollment.student} - {self.date}"

    class Meta:
        unique_together = ('enrollment', 'date')


# class Exam(models.Model):
#     enrollment = models.ForeignKey('Home.Enrollment', on_delete=models.CASCADE)
#     date = models.DateField()
#     subject = models.CharField(max_length=255)
#     marks = models.DecimalField(max_digits=5, decimal_places=2)


class Library(models.Model):
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_publisher = models.CharField(max_length=255)
    book_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.book_title} - {self.book_author}"


class BookIssue(models.Model):
    enrollment = models.ForeignKey('Home.Enrollment', on_delete=models.CASCADE)
    book = models.ForeignKey('Home.Library', on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    staff = models.ForeignKey('Home.Staff', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.enrollment.student} - {self.book.book_title}"


class Finance(models.Model):
    enrollment = models.ForeignKey('Home.Enrollment', on_delete=models.CASCADE)
    paid_fee = models.DecimalField(max_digits=10, decimal_places=2)
    fee_submitted_date = models.DateTimeField(blank=True, null=True)

    @property
    def total_fee(self):
        return self.enrollment.course.total_fee

    @property
    def remaining_fee(self):
        return self.total_fee - self.paid_fee

    def save(self, *args, **kwargs):
        if self.paid_fee > 0 and not self.fee_submitted_date:
            self.fee_submitted_date = timezone.now()
        super(Finance, self).save(*args, **kwargs)


class Placement(models.Model):
    enrollment = models.ForeignKey('Home.Enrollment', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_placement = models.DateField()
