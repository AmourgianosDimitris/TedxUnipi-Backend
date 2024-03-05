# from django.test import TestCase
import datetime

# Create your tests here.
value = 2019
if value not in range(2015, datetime.date.today().year+1):
    print ("True")
    # raise ValidationError(
    #     _('%(value)s is not an even number'),
    #     params={'value': value},
    # )
