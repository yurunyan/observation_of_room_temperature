from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
import pandas as pd
import matplotlib.pyplot as plt
import io, os


def getsvg():
    abspath = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(f'{abspath}/Temperature.csv', header=None)
    df.columns = ['time', 'temp', 'pressure', 'humidity']
    svg = ''
    for name in ['temp', 'humidity', 'pressure']:
        _, ax = plt.subplots(figsize=(15,3))
        ax.plot([x[11:16] for x in df['time'][::-1]], df[name][::-1])
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=60, fontsize=10)
        plt.setp(labels[1::6], rotation=60, fontsize=3)
        plt.setp([x for i, x in enumerate(labels) if i % 6 != 0], rotation=60, fontsize=6)
        plt.title(name)
        buf = io.BytesIO()
        plt.savefig(buf, format='svg', bbox_inches='tight')
        s = buf.getvalue()
        buf.close()
        svg += s.decode('utf-8')
        #plt.show()
    return svg

def temp(request):
    data = request.GET.get(key="observationdata", default=None)
    if data is not None:
        abspath = os.path.dirname(os.path.abspath(__file__))
        with open(f'{abspath}/Temperature.csv', 'w') as f:
            f.write(data)
        return HttpResponse('Done')
    else:
        return HttpResponse(getsvg())
