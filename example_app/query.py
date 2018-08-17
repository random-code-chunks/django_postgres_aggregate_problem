import collections

from django.db.models import QuerySet, Case, When, Q, Value, CharField, Count


class RunInfoQuerySet(QuerySet):
    def annotate_status(self):
        good_criteria = ['Good', 'Lowstat']

        return self.annotate(status=Case(
            When(
                (Q(type__runtype="Cosmics") | Q(pixel__in=good_criteria)) &
                Q(sistrip__in=good_criteria) &
                Q(tracking__in=good_criteria),
                then=Value('good')),
            default=Value('bad'),
            output_field=CharField())
        )

    def filter_flag_changed(self, until=None):
        """
        Filters the queryset to all runs where the flag has changed
        """

        from example_app.models import RunInfo
        # Group by unique run_number, status pairs
        # if a run_number appears more than once, it means that the flag changed

        runs = RunInfo.objects.all()

        run_number_list = [run["run_number"]
                           for run
                           in self \
                               .order_by("run_number") \
                               .values("run_number")]
        return self
