def my_function(request):
    return 'Hello World'
functions-framework --target my_function
curl http://localhost:8080
def hello(request):
if request.args:
    return f'Hello' + request.args.get('first') + request.args.get('last')+'\n'
elif request.get_json():
        request_json = request.get_json()
        return  f'Hello' + request_json['first'] + request_json['last']+'\n'
elif request.values:
    request_data = request.values
    return  f'Hello' + request_data['first'] + request_data['last']+'\n'
else:
    return f'Hello World!'+'\n'

curl http://localhost:8080?first=My&last=Name


http://localhost:8080