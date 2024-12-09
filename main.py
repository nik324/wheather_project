from requests import get
from flask import Flask, render_template, request, jsonify
cords = []
key_loc = ""
app = Flask(__name__)
@app.route('/', methods=['PUT', 'GET', 'POST'])
def hey():
    if request.method == 'GET':
        return render_template('Hello.html')
@app.route('/add', methods=['PUT', 'GET', 'POST'])
def first():
    if request.method == 'GET':
        return render_template('FirstPage.html')
    else:
        try:
            a = abs(float(request.form['lat']))
            b = abs(float(request.form['lon']))
        except ValueError:
            return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."

        except TypeError:
            return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."
        if (a <= 90 and b <= 180):
            cords.append({'latitude': request.form['lat'], 'longitude': request.form['lon']})
            params = {
                'apikey': "8Jn522PtNaWDaiJrEAfEpg1K9KxM2Ubo",
                'q': str(a) + ',' + str(b)
            }
            r = get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search', params=params)
            if r.status_code == 200:
                key_loc = r.json()['Key']
                apik = "8Jn522PtNaWDaiJrEAfEpg1K9KxM2Ubo"
                url = 'http://dataservice.accuweather.com/currentconditions/v1/' + key_loc
                forecast = get(url, params={'apikey':apik, 'details':'true'}).json()
                temp = forecast[0]['Temperature']['Metric']['Value']
                perc = forecast[0]['HasPrecipitation']
                visible = forecast[0]['Visibility']['Metric']
                wind = forecast[0]['WindGust']['Speed']['Metric']
                if temp < 30 and temp > -10 and  not perc and visible['Value'] > 1 and visible['Unit'] == 'km' and wind < 10:
                    return "Погода чудесная. Пора ехать"
                else:
                    return "Поездку лучше отложить"
            else:
                return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."

        else:
            return "Координаты введены в неправильном формате. Что бы успешно добавить точку снова перейди на /add и введи координаты в формате числа с разделенной точкой дробной частью. Если твоя точка в южном или западном полушарии, то вводи соответсвующие координаты с минусом."

@app.route('/data', methods=['PUT', 'GET', 'POST'])
def data():
    if request.method == 'GET':
        return jsonify(cords)
if __name__ == '__main__':
    app.run(debug=True)




