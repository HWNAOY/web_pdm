import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUpload
import json
# our home page view


def home(request):
    return render(request, 'index.html')


def my_ml_algorithm(file):

    df = pd.read_excel(file)

    X = df.drop('Volume', axis=1)
    y = df['Volume']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    model = LinearRegression().fit(X_train, y_train)

    prediction = pd.DataFrame(model.predict(X_test))
    return prediction


def upload_file(request):

    if request.method == 'POST':

        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():

            # Save the uploaded file to a FileField in the database
            # form.save()
            # Call the machine learning algorithm on the uploaded file
            result = my_ml_algorithm(form.cleaned_data['file'])
            # json_records = result.reset_index().to_json(orient ='records')
            # data = []
            # data = json.loads(json_records)
            data = result.to_html()
            context = {'data': data}
            # Render a template that displays the results of the algorithm
            return render(request, 'result.html', context)
            # return render(request, 'result.html', {'result': result.to_html()})

    else:
        form = FileUpload()
    return render(request, 'upload.html', {'form': form})
