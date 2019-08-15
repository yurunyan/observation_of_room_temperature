from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
import pandas as pd
import matplotlib.pyplot as plt
import io, os, tempfile
import threading


def getsvg(df):
    df.columns = ['time', 'temp', 'pressure', 'humidity']
    svg = ''

    _, ax1 = plt.subplots(figsize=(15,6))
    ax1.plot([x[11:16] for x in df['time'][::-1]], df['temp'][::-1], label='temperature')
    labels = ax1.get_xticklabels()
    ax2 = ax1.twinx()
    ax2.plot([x[11:16] for x in df['time'][::-1]], df['humidity'][::-1], color='purple', label='humidity')
    ax1.legend(loc='upper left')
    ax2.legend(loc='center left')
    plt.setp(labels, rotation=60, fontsize=10)
    plt.setp(labels[1::6], rotation=60, fontsize=10)
    plt.setp([x for i, x in enumerate(labels) if i % 6 != 1], rotation=60, fontsize=1)
    plt.title('temperature and humidity')

    with io.BytesIO() as buf:
        plt.savefig(buf, format='svg', bbox_inches='tight')
        s = buf.getvalue()
        
    svg += s.decode('utf-8')
    #plt.show()

    _, ax3 = plt.subplots(figsize=(15,3))
    ax3.plot([x[11:16] for x in df['time'][::-1]], df['pressure'][::-1], label='pressure')
    labels = ax3.get_xticklabels()
    plt.setp(labels, rotation=60, fontsize=10)
    plt.setp(labels[1::6], rotation=60, fontsize=10)
    plt.setp([x for i, x in enumerate(labels) if i % 6 != 1], rotation=60, fontsize=1)
    plt.title('air pressure')

    with io.BytesIO() as buf:
        plt.savefig(buf, format='svg', bbox_inches='tight')
        s = buf.getvalue()
    #buf.close()
    svg += s.decode('utf-8')

    return svg

def write_html(data):
    abspath = os.path.dirname(os.path.abspath(__file__))
    with tempfile.TemporaryDirectory() as dname:
        x = f'{dname}/temp.txt'
        with open(x, 'w') as f:
            f.write(data)
        df = pd.read_csv(x, header=None)
    with open(f'{abspath}/Temperature.html', 'w') as f:
        f.write(getsvg(df))    

def temp(request):
    abspath = os.path.dirname(os.path.abspath(__file__))
    data = request.GET.get(key="observationdata", default=None)
    if data is not None:
        t1 = threading.Thread(target=write_html, args=(data,))
        t1.start()
        return HttpResponse('Done')
    else:
        with open(f'{abspath}/Temperature.html', 'r') as f:
            data = f.read()
        return HttpResponse('<title>部屋の空気</title>' + data)
