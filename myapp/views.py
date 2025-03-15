from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User,Courses,Cart
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.core.mail import send_mail

def chat_room(request):
    return render(request, "chat.html")

def send_sms(request):
    url = "add_fast2sms_url"
    payload = {
        "message": "Hello from Django!",
        "language": "english",
        "route": "q",
        "numbers": "123456789"  # Replace with your number
    }
    headers = {
        "authorization": "Add_Auth__for_fast_2_sms",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    messages.error(request,response.json())
    return redirect("home")

def apiCheck(request):
    admin = False
    first_letter = "L"  # Default name
    
    if 'email' in request.session:
        try:
            user = User.objects.get(email=request.session['email'])
            first_letter = request.session.get('name', 'L')[0].upper()
            if user.usertype == "admin":
                admin = True
        except User.DoesNotExist:
            pass  # Handle case where user is not found
    
    outvalue = ""
    
    if request.method == "POST":
        try:
            API_KEY = "API_KEY"  # Replace with a secure method
            URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            data = {"contents": [{"parts": [{"text": request.POST['ptp']}]}]}
            
            response = requests.post(URL, json=data)
            response_data = response.json()

            if "candidates" in response_data:
                outvalue = response_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                outvalue = "Error: No response from API"
        
        except requests.exceptions.RequestException as e:
            outvalue = f"API request failed: {str(e)}"
    #print(outvalue)
    
    return render(request, 'apiCheck.html', {'name': first_letter, 'outvalue': outvalue, 'admin': admin})


def send_email_to_user(request):
    if 'email' in request.session:
        user_email = request.session['email']  # Get the logged-in user's email

        subject = "Hello from Django!"
        message = f"Hi {request.session['name']},\n\nThis is a test email from your Django project."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]

        send_mail(subject, message, from_email, recipient_list)
        messages.error(request,'Email Sent Successfully')
        return redirect("home")  # Redirect to any page after sending the emai
    else:
         messages.error(request,'Login First')
         return redirect('home')


class Node:
    def __init__(self, course):
        self.course = course
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, course):
        new_node = Node(course)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        courses_list = []
        current = self.head
        while current:
            courses_list.append(current.course)
            current = current.next
        return courses_list

def get_popular_courses():
    courses = Courses.objects.all()
    popular_list = LinkedList()
    
    for course in courses:
        if course.course_bought >= 8:
            popular_list.append(course)

    return popular_list.to_list()

def get_free_courses():
    courses=Courses.objects.all()
    free_list=LinkedList()
    for i in courses:
        if i.course_price==0:
            free_list.append(i)
    return free_list.to_list()

def get_course_names():
    courses=Courses.objects.all()
    names=LinkedList()
    for i in courses:
        names.append(i.course_name)
    return names.to_list()

def home(request):
    popularList = get_popular_courses()
    freeList=get_free_courses()
    namesList=get_course_names()
    if 'email' in request.session:
        user=User.objects.get(email=request.session['email'])
        first_letter = request.session['name'][0].upper()
        admin=False
        if user.usertype=="admin":
            admin=True
        return render(request,'home.html',{'name':first_letter,'admin':admin,'popular':popularList,'free':freeList,'course_names':namesList})
    else:
        return render(request,'home.html',{'name':"L",'popular':popularList,'free':freeList,'course_names':namesList})

def profile(request):
    msg, name = "", ""
    admin = False
    if 'email' in request.session:
        try:
            user = User.objects.get(email=request.session['email'])
            
            name = user.name[0] 

            if user.usertype == "admin":
                admin = True
            return redirect('logout')
        
        except:
            return redirect('logout')
    else:
        return redirect('login')

def search(request):
    msg=""
    admin=True
    name=""
    try:
        user=request.session['email']
        name=user.name[0]
    except:
        admin=False
        name="L"
    search_text=request.POST['searchInput']
    check=search_text.lower()
    if check=="login":
        return redirect('login')
    elif check=='signup':
        return redirect('signup')
    elif check=='course' or check=='courses':
        return redirect('courses')
    else:
        if check=="":
            messages.error(request,'Search Empty')
            return redirect('home')
        courses=Courses.objects.all()
        list=[]
        for i in courses:
            if i.course_name.lower().startswith(check):
                list.append(i)
        if len(list)==0:
            messages.error(request, "Search yielded 0 results .")
            return redirect('home')
        else:
            return render(request,'allCourses.html',{'msg':msg,'cour':list,'name':name,'admin':admin})
    
def courses(request):
    msg=""
    name=""
    c=Courses.objects.all()
    try:
        if request.session['email']:
            user=User.objects.get(email=request.session['email'])
            name=user.name[0]
            if user.usertype=="admin":
                return render(request,'allCourses.html',{'msg':msg,'cour':c,'name':name,'admin':True})
            else:
                return render(request,'allCourses.html',{'msg':msg,'cour':c,'name':name,'admin':False})

    except:
        name="L"
        return render(request,'allCourses.html',{'msg':msg,'cour':c,'name':name,'admin':False})

def admin_page(request):
    user=User.objects.get(email=request.session['email'])
    msg=""
    return render(request,'admin.html',{'msg':msg,'name':user.name[0],'admin':True})

def contact(request):
    msg=""
    admin=False
    name=""
    if 'email' in request.session:
        user=User.objects.get(email=request.session['email'])
        name=user.name[0]
        if user.usertype=='admin':
            admin=True
    else:
        name="L"
    return render(request,'contactPage.html',{'msg':msg,'name':name,
                                              'admin':admin})

def add_course(request):
    msg=""
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
       try: 
           input=request.POST['just']
           return render(request,'admin_addCourse.html',{'msg':msg,'admin':True,'name':user.name[0]})
       except Exception as e: 
           Courses.objects.create(
            course_name=request.POST['c_name'],
            course_price=float(request.POST['c_price']),
            course_length=request.POST['c_length'],
            course_img=request.FILES['c_img']
            )
           msg="Course added"
           return render(request,'admin_addCourse.html',{'msg':msg,'admin':True,'name':user.name[0]})
    else:
        return render(request,'admin.html',{'msg':msg,'admin':True,'name':user.name[0]})
    
def update_course(request):
    msg=""
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
       try:
            if request.POST['just']:
                return render(request,'admin_updateCourse.html',{'msg':msg,'admin':True,'name':user.name[0]})
       except:
            c_id=request.POST['c_id']
            try:
                course_object=Courses.objects.get(course_id=c_id)
                return render(request,'admin_properUpdate.html',{'msg':msg,'admin':True,'name':user.name[0],
                                                                    'course_object':course_object})
            except:
                msg="Course id not found"
                return render(request,'admin_updateCourse.html',{'msg':msg,'admin':True,'name':user.name[0]})
    else:
       return render(request,'admin_updateCourse.html',{'msg':msg,'admin':True,'name':user.name[0]})
   
def proper_update(request):
    msg=""
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        c_id=request.POST['id']
        C_Object=Courses.objects.get(course_id=c_id)
        C_Object.course_name=request.POST['c_name']
        C_Object.course_price=request.POST['c_price']
        C_Object.course_length=request.POST['c_length']
        try:
            C_Object.course_img=request.FILES['c_image']
        except:
            pass
        C_Object.save()
        msg="Course info updated"
        return render(request,'admin.html',{'msg':msg,'admin':True,'name':user.name[0]})
    else:
        return render(request,'admin_properUpdate.html',{'msg':msg,'admin':True,'name':user.name[0]})

def delete_course(request):
    msg=""
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        try:
            if request.POST['just']:
                return render(request,'admin_deleteCourse.html',{'msg':msg,'admin':True,'name':user.name[0]})
        except:
            c_id=request.POST['cid']
            try:
                Courses.objects.get(course_id=c_id).delete()
                msg="Course Deleted"
            except:
                msg="Course not found"
            return render(request,'admin_deleteCourse.html',{'msg':msg,'admin':True,'name':user.name[0]})
    else:
         return render(request,'admin_properUpdate.html',{'msg':msg,'admin':True,'name':user.name[0]})

def logout(request):
    try:
        del request.session['email']
        del request.session['name']
        del request.session['password']
        msg = "User logged out Successfully"
        return render(request, 'login.html', {'msg': msg,'name':"L"})
    except:
        msg = "User logged out Successfully"
        return render(request, 'login.html', {'msg': msg,'name':"L"})        

def login(request):
    if request.method=="POST":
        try:
            emails=User.objects.values_list('email',flat=True)
            if request.POST['email'] in emails:
                user=User.objects.get(email=request.POST['email'])
                if user.password==request.POST['password']:
                    request.session['email']=request.POST['email']
                    request.session['name']=user.name
                    request.session['password']=request.POST['password']
                    msg="User logged in succesfully"
                    course=Courses.objects.all()
                    most=[]
                    free=[]
                    for i in course:
                        if i.course_bought>=8:
                            most.append(i)
                        if i.course_price==0:
                            free.append(i)
                    admin=False
                    if user.usertype=="admin":
                        admin=True
                    return render(request,'home.html',{'msg':msg,'name':user.name[0].upper(),'admin':admin,'popular':most,'free':free})
                else:
                    msg='Wrong password'
                    return render(request,'login.html',{'msg':msg,'name':"L"})
            else:
                msg="Email not registered"
                return render(request,'login.html',{'msg':msg,'name':"L"})
        except Exception as e:
            msg="Something went wrong "+str(e)
            return render(request,'login.html',{'msg':msg,'name':"L"})
    else:
        if 'emails' in request.session:
            user=User.objects.get(email=request.session['email'])
            return render(request,'login.html',{'name':user.name[0].upper()})
        else:
            return render(request,'login.html',{'name':"L"})

def signup(request):
    if request.method=="POST":
        try:
            emails = User.objects.values_list('email', flat=True)
            if request.POST['email'] not in emails:
                if request.POST['password']==request.POST['confirm_password']:
                    User.objects.create(
                        email=request.POST['email'],
                        password=request.POST['password'],
                        name=request.POST['name']
                    )
                    msg='Signup Succesful'
                    return render(request,'signup.html',{'msg':msg,'name':"L"})
                else:
                    msg='Password and Confirm password do not match'
                    return render(request,'signup.html',{'msg':msg,'name':"L"})
            else:
                msg="Email already registered"
                return render(request,'signup.html',{'msg':msg,'name':"L"})
        except Exception as e:
            msg="Something went wrong "+str(e)
            return render(request,'signup.html',{'msg':msg,'name':"L"})
    else:
        return render(request,'signup.html',{'name':"L"})
    
def cart_page(request):
    if request.method=="POST":
         user=User.objects.get(email=request.session['email'])
         admin=False
         if user.usertype=="admin":
             admin=True
         id=request.POST['c_id']
         catr=Cart.objects.filter(email_use=user.email,course_IDS=id)
         catr.delete()
         c=Cart.objects.filter(email_use=user.email)
         course_ids = [cart.course_IDS for cart in c]
         if len(course_ids)==0:
              messages.error(request, "Cart is Empty  , must add a item to cart before vieweing")
              return redirect('home')
         courses = Courses.objects.filter(course_id__in=course_ids) 
         return render(request,'userCart.html',{'courses':courses,'admin':admin,'name':user.name[0]}) 
    else:
         user=User.objects.get(email=request.session['email'])
         c=Cart.objects.filter(email_use=user.email)
         course_ids = [cart.course_IDS for cart in c]
         if len(course_ids)==0:
            messages.error(request, "Cart is Empty  , must add a item to cart before vieweing")
            return redirect('home')
         courses = Courses.objects.filter(course_id__in=course_ids)  
         admin=False
         if user.usertype=="admin":
             admin=True
         return render(request,'userCart.html',{'courses':courses,'admin':admin,'name':user.name[0]})

def check_cart(request,cid):
   return Cart.objects.filter(email_use=request.session['email'], course_IDS=cid).exists()

def middle_cart(request):
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])
        coid = request.POST['coid']
        if check_cart(request,coid):
            msg="Course already in Cart"
            c=Courses.objects.all()
            user=User.objects.get(email=request.session['email'])
            name=user.name[0]
            admin=False
            if user.usertype=="admin":
                admin=True
            return render(request,'allCourses.html',{'msg':msg,'cour':c,'name':name,'admin':admin})
        Cart.objects.create(email_use=user.email, course_IDS=coid)
        return redirect('cartPage')
    return redirect('login')  


def buy(request):
    user=User.objects.get(email=request.session['email'])
    carting=Cart.objects.filter(email_use=user.email)
    names=[]
    check=True
    msg=""
    if len(carting)==0:
        check=False
        msg="Cart is empty"
    products=[]
    for i in carting:
        c=Courses.objects.get(course_id=i.course_IDS)
        products.append(c.course_price)
        c.course_bought+=1
        c.save()
    totalprice=sum(products)
    Cart.objects.filter(email_use=user.email).delete()
    course=Courses.objects.all()
    admin=False
    if user.usertype=="admin":
        admin=True
    return render(request,'allCourses.html',{'msg':msg,'name':user.name[0],'cour':course,'admin':admin,'bought':totalprice,'check':check})