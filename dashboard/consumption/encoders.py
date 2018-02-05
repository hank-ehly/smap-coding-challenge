from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text

from consumption.models import ConsumptionRollup


class ConsumptionRollupEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ConsumptionRollup):
            return force_text(obj)
        return super(ConsumptionRollupEncoder, self).default(obj)
