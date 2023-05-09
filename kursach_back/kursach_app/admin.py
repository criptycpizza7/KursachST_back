from django.contrib import admin
from .models import Company, Portfolio, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("username", "is_staff")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ('Name', 'Ticker', 'Picture', 'Number_of_shares', 'Country', 'Currency')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    fields = ('User_id', 'Company_id', 'Number_of_shares')
