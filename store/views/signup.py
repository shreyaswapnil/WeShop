from django.shortcuts import render, redirect

from django.contrib.auth.hashers import make_password

from store.models.customer import Customer
from django.views import View



class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')

    def post(self,request):
        postData = request.POST

        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # dictionary for storing all values
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': password

        }
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name,
                            phone=phone, email=email, password=password)

        error_message = self.validateCustomer(customer)
        # saving

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
            # return render(request,'index.html')
            # return HttpResponse("Account created!")
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self,customer):
        # validation cases
        error_message = None
        if (not customer.first_name):
            error_message = "First Name is required!"
        elif len(customer.first_name) < 4:
            error_message = "First Name should be at least 4 characters long"
        elif (not customer.last_name):
            error_message = "Last Name is required!"
        elif len(customer.last_name) < 4:
            error_message = "Last Name should be at least 4 characters long"
        if (not customer.phone):
            error_message = "Phone Number is required!"
        elif len(customer.phone) < 10:
            error_message = "Phone number should have at least 10 characters"
        elif len(customer.password) < 4:
            error_message = "Password should be at least 6 characters long"
        elif len(customer.email) < 5:
            error_message = "Email id should be at least 4 characters long"
        elif customer.alreadyExists():
            error_message = 'Email Address Already Registered!'

        return error_message