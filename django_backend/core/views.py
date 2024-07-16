from django.shortcuts import render
# Custom model imports
from cars.models import Car


# Index (home) view
def index(request):
    """ A view to return the index page """
    # Road collcetion Car stats
    # Road collcetion Events stats
    context = {
        # Road collcetion cars stats
        # Road collcetion events stats
    }

    return render(request, 'core/index.html', context)