from django.shortcuts import render
from blog.models import BlogsPost,Exchange_record,Infect_source
from django.http import HttpResponse,HttpResponseRedirect
import time
record_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def blog_index(request):
    blog_list = BlogsPost.objects.all()
    return render(request,'index.html',{'blog_list':blog_list})
def About(request):
    return render(request,'About.html')
def ShowResults(request):
    if request.method == 'POST' and ( 'q' in request.POST):
        if request.POST['q'] :
            # if data is true ,we should solve the data ,example save
            # print(request.POST['q'])
            if len(request.POST['q'].split( )) == 2:
                title = request.POST['q'].split( )[0]
                body = request.POST['q'].split( )[1]
                
                context = title + ' ' + body

                record_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                timestamp_s = time.time()

                Exchange_record.objects.create(context = context,timestamp = record_date,timestamp_s = timestamp_s)
                
                if BlogsPost.objects.filter(title = title):
                    if BlogsPost.objects.filter(title = body):
                        temp1 = BlogsPost.objects.get(title = title).body 
                        temp2 = BlogsPost.objects.get(title = body).body

                        temp_title = temp1 + ' ' + body + ' ' + temp2 
                        BlogsPost.objects.filter(title = title).update(body = temp_title)

                        temp_body = temp2 + ' ' + title + ' ' + temp1
                        BlogsPost.objects.filter(title = body).update(body = temp_body)
                    else:
                        temp1 = BlogsPost.objects.get(title = title).body 

                        temp_title = temp1 + ' ' + body
                        BlogsPost.objects.filter(title = title).update(body = temp_title)

                        temp_body = title + ' ' + temp1

                        BlogsPost.objects.create(title = body , body = temp_body ,timestamp = record_date,timestamp_s = timestamp_s)

                else:
                    if BlogsPost.objects.filter(title = body):
                        
                        temp2 = BlogsPost.objects.get(title = body).body

                        temp_title = body + ' ' + temp2
                        BlogsPost.objects.create(title = title , body = temp_title ,timestamp = record_date,timestamp_s = timestamp_s)
                        

                        temp_body =  temp2 + ' ' + title
                        BlogsPost.objects.filter(title = body).update(body = temp_body)
                    else:
                    
                       BlogsPost.objects.create(title = title , body = body ,timestamp = record_date,timestamp_s = timestamp_s)

                       BlogsPost.objects.create(title = body , body = title ,timestamp = record_date,timestamp_s = timestamp_s)
            

            return render(request,'success.html',{'suc':request.POST['q']})
        else:#if input is blank then go to the initial site
            return HttpResponseRedirect('/inputGen')


        # blog_list = BlogsPost.objects.all()
        # return render(request,'ShowResults.html',{'blog_list':blog_list})
    else:
        # BlogsPost.objects.create(title = 'z',body  = '111',timestamp = record_date)
        # Exchange_record = Exchange_record.objects.all()

        if Exchange_record.objects.all():
            return render(request,'ShowResults.html',{'Exchange_list':Exchange_record.objects.all()})
            
        else:
            return render(request,'errorresults.html')
    
def influence(request):

    # 需要实时的读取数据库并显示信息
    #
    d = {} 
    blog_list = BlogsPost.objects.all()
    a = Infect_source.objects.get( id = 1).infect_id

    for i in blog_list:
        if a in i.title or a in i.body:
            d[i.title] = '感染'
        else:
            d[i.title] = '健康'


    dsort = sorted(d.items())

    e = {}
    
    for i in dsort:
        e[i[0]] = d[i[0]]


    return render(request,'influence.html',{'influence':dsort})




    return render(request,'influence.html')
def testdb(request):

    blog_list = BlogsPost.objects.all()
    flag = 0
    for i in blog_list:
        if i.title == 'X' and i.body == '111':
            flag = 1
    if flag == 0:
        BlogsPost.objects.create(title = 'z',body  = '111',timestamp = record_date)
    return render(request,'index.html')
# Create your views here.
