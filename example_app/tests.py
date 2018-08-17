from django.db.models import Count, Case, When, Value, CharField
from django.test import TestCase

from example_app.models import MyModel


# Create your tests here.
class TestMyModel(TestCase):
    def setUp(self):
        MyModel.objects.create(attribute_a=1)
        MyModel.objects.create(attribute_a=1)
        MyModel.objects.create(attribute_a=4)

    def test_no_count(self):
        my_list = [1]
        mymodels = MyModel.objects \
            .annotate(my_annotation=Case(
            When(attribute_a__in=my_list,
                 then=Value('yes')),
            default=Value('no'),
            output_field=CharField())
        ) \
            .values("my_annotation")
        print(mymodels)

    def test_case_and_count(self):
        my_list = [1]
        mymodels = MyModel.objects.annotate(my_annotation=Case(
            When(attribute_a__in=my_list,
                 then=Value('yes')),
            default=Value('no'),
            output_field=CharField())
        )
        mymodels = mymodels.values("my_annotation")\
            .annotate(count_a=Count("my_annotation"))
        print(mymodels)

    def test_case_and_count_no_values(self):
        my_models = MyModel.objects \
            .annotate(my_annotation=Case(
            When(attribute_a__in=[1], then=Value('yes')),
            default=Value('no'),
            output_field=CharField())
        ) \
            .annotate(count_a=Count("my_annotation"))
        print(my_models)

    def test_just_count(self):
        mymodels = MyModel.objects \
            .values("attribute_a") \
            .annotate(count_a=Count("attribute_a"))
        print(mymodels)
