
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from managerbook.models import *
from managerbook.form import *
from django.forms import model_to_dict
from PIL import Image

class Edit_Book(View):
    def get(self, request, book_id):
        """
        回显数据
        :param request:
        :return:
        """
        author_id = []
        book_id = int(book_id)
        book = Book.objects.get(id=book_id)
        book_dict = model_to_dict(book)

        author_list = book_dict['author']
        for author_obj in author_list:
            author_id.append(author_obj.id)

        try:
            details = Details.objects.get(id=int(book_dict['info']))
            details_dict = model_to_dict(details)
            details_form = DetailsForm(initial=details_dict)
        except:
            details_form = DetailsForm()
            details = None

        book_dict['author'] = author_id
        book_form = BookForm(initial=book_dict)

        return render(request, 'book_edit.html', {
            'book_form': book_form,
            'details_form': details_form,
            'book_id': book_id,
            'details': details,
        })

    def post(self, request, book_id):
        """
        提交更改数据
        几种更新：
            1.带图片更新已有的书籍详情信息　（替换已有的图片）
            2.不带图片更新已有的书籍详情信息 （新上传一个图片）
                (1) 更新已有的书籍详情信息(try捕捉错误处理图片)
            3.没有创建图书详情信息  (创建一个图书详情信息，上传图片)
            4.没有创建图书详情信息且不上传图片的 (创建一个图书详情信息，不上传图片)
                (2) 创建图书详情信息(try捕捉错误处理图片)
        更新流程：
            1.获取用户提交POST值并且传入我们的表单
            2.双表单的验证 book_form.is_valid()=True and details_form.is_valid()=True
            3.更新(4种情况)
        :param request:
        :return:
        """
        details_form = DetailsForm(request.POST, request.FILES)
        book_form = BookForm(request.POST)

        if details_form.is_valid() and book_form.is_valid():
            """
            双表单的验证
            """
            book_data = book_form.cleaned_data
            details_data = details_form.cleaned_data

            """拿到book queryset要进行update"""
            book = Book.objects.filter(id=int(book_id))

            try:
                """拿到这本书的详情信息，如果执行try里面的代码，
                就代表要更新详情信息，如果执行except就是创建详情信息
                """
                details = Details.objects.filter(id=int(book[0].info_id))
            except:
                details = None

            """对book进行update更新"""
            book.update(
                name=book_data['name'],
                publish_year=book_data['publish_year'],
                publish_add=book_data['publish_add'],
                price=book_data['price'],
                stocks=book_data['stocks'],
                status=book_data['status'],
                type_id=book_data['type'],
                publisher_id=book_data['publisher'],
            )

            # 多对多作者更新处理
            book[0].author.set(book_data['author'])



            if details:
                """
                更新书籍详情信息
                """
                try:
                    """
                    如果执行try里面的代码，就代表要更新图片，
                    反之执行except里面的代码，就代表不更新图片。
                    """
                    # 图片处理
                    logo = request.FILES['logo']
                    location = 'images/' + \
                               str(details_data['words']) + str(details_data['pages']) + '_' + str(logo.name)
                    img = Image.open(logo)
                    img.save(location)

                    details.update(
                        chapter=details_data['chapter'],
                        contentinfo=details_data['contentinfo'],
                        catalog=details_data['catalog'],
                        words=details_data['words'],
                        pages=details_data['pages'],
                        logo=location
                    )
                except:
                    details.update(
                        chapter=details_data['chapter'],
                        contentinfo=details_data['contentinfo'],
                        catalog=details_data['catalog'],
                        words=details_data['words'],
                        pages=details_data['pages'],
                    )

                return render(request, 'book_edit.html', {
                    'book_form': book_form,
                    'details_form': details_form,
                    'details': details[0],
                    'book_id': book_id,
                })
            else:
                """
                创建书籍详情信息
                """
                # 实例化一个Details对象，用于后面的创建保存
                details = Details()

                # 拿到当前这本书的book对象，用于后面的详情信息与书籍绑定
                book_obj = Book.objects.get(id=int(book_id))

                try:
                    """
                    如果执行try里面的代码，
                    创建一条details记录，
                    同时要绑定到当前这本书(把这个书籍详情信息对应到这本书上)，

                    反之如果执行except里面的代码，
                    创建一条不带图片的details记录，
                    同时要绑定到当前这本书(把这个书籍详情信息对应到这本书上)，
                    """
                    # 处理图片
                    logo = request.FILES['logo']
                    location = 'images/' + \
                               str(details_data['words']) + str(details_data['pages']) + '_' + str(logo.name)
                    img = Image.open(logo)
                    img.save(location)

                    details.chapter = details_data['chapter']
                    details.contentinfo = details_data['contentinfo']
                    details.catalog = details_data['catalog']
                    details.words = details_data['words']
                    details.pages = details_data['pages']
                    details.logo = location
                    details.save()

                    book_obj.info = details
                    book_obj.save()
                except:

                    details.chapter = details_data['chapter']
                    details.contentinfo = details_data['contentinfo']
                    details.catalog = details_data['catalog']
                    details.words = details_data['words']
                    details.pages = details_data['pages']
                    details.save()

                    book_obj.info = details
                    book_obj.save()

                return render(request, 'book_edit.html', {
                    'book_form': book_form,
                    'details_form': details_form,
                    'details': details,
                    'book_id': book_id,
                })


class Book_Del(View):
    """
    书籍删除功能
    """
    def post(self, request):
        ret = {'status': "success", "data": "删除成功"}

        book_id = request.POST.get('book_id')
        book_id = int(book_id)

        book_obj = Book.objects.get(id=book_id)
        book_obj.delete()

        return JsonResponse(ret)




class Create_Details(View):
    """
    完善书籍详情页功能
    """
    def post(self, request):
        ret = {'status': "", "data": ""}

        details_form = DetailsForm(request.POST, request.FILES)

        if details_form.is_valid():
            details_data = details_form.cleaned_data
            details = Details()
            details.chapter = details_data['chapter']
            details.contentinfo = details_data['contentinfo']
            details.catalog = details_data['catalog']
            details.words = details_data['words']
            details.pages = details_data['pages']

            # 保存图片
            logo = details_data['logo']
            location = 'images/' + \
                       str(details_data['words']) + str(details_data['pages']) + '_' + str(logo.name)
            img = Image.open(logo)
            img.save(location)

            # 存储数据库路径
            details.logo = location
            details.save()

            # 关联我们当前这本书的详细信息
            book_obj = Book.objects.get(id=int(request.POST.get('book_id')))
            book_obj.info = details
            book_obj.save()

            ret['status'] = 'success'
            ret['data'] = '图书信息完善成功'
            return  JsonResponse(ret)



        else:
            ret['data'] = details_form.errors

            return JsonResponse(ret)


class Addbook(ListView):
    template_name = 'add_book.html'
    model = Book
    context_object_name = 'book_obj'

    def get_queryset(self):
        quryset = super(Addbook, self).get_queryset()

        page = self.request.GET.get('page', 1)
        p = Paginator(quryset, 10)
        people = p.page(page)

        return people


    def get_context_data(self, **kwargs):
        book_form = BookForm()
        details_form = DetailsForm()
        context = super(Addbook, self).get_context_data()

        context['book_form'] = book_form
        context['details_form'] = details_form

        return context

    def post(self, request):
        ret = {"status": "", "data": ""}
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            book_data = book_form.cleaned_data
            book = Book()
            book.name = book_data['name']
            book.publish_year = book_data['publish_year']
            book.price = book_data['price']
            book.stocks = book_data['stocks']
            book.status = book_data['status']
            book.type_id = book_data['type']
            book.publisher_id = book_data['publisher']
            book.save()

            book.author.add(*book_data['author'])

            ret['status'] = "success"
            ret['data'] = '书籍添加成功'

            return JsonResponse(ret)
        else:
            print(book_form.errors)
            ret['data'] = book_form.errors
            """
            {
                'status': "",
                'data': "{"price": '必须要填写的值'},"
            }
            """
            return JsonResponse(ret)

class index(ListView):
    """
    首页 书籍列表 查询功能
    """
    template_name = 'book.html'
    # Book.objects.all()
    model = Book
    context_object_name = 'book_obj'

    def get_queryset(self):
        # super代表，调用父类的
        queryset = super(index, self).get_queryset()
        # queryset == Book.objects.all()
        # queryset 就是等同于，取出Book表中所有的值

        # page = self.request.GET.get('page', 1)
        #
        # # 第一个参数 数据[] list,
        # # 第二个参数 request  请求
        # # 第三个参数 一页展示多少条
        # p = Paginator(queryset, request=self.request, per_page=10)
        #
        # people = p.page(page)
        page = self.request.GET.get('page', 1)

        self.is_type = self.request.GET.get('type', '')
        self.search = self.request.GET.get('search', '')

        # Q 多种条件查询
        #  and == &
        #  or == |

        if self.is_type and self.search:
            queryset = self.model.objects.filter(
                (Q(name__icontains=self.search) | Q(author__name__icontains=self.search))
                & Q(type=self.is_type)
            ).distinct()
        elif self.is_type:
            queryset = self.model.objects.filter(
                (Q(name__icontains=self.search) | Q(author__name__icontains=self.search))
                & Q(type=self.is_type)
            ).distinct()
        elif self.search:
            queryset = self.model.objects.filter(
                (Q(name__icontains=self.search) | Q(author__name__icontains=self.search))

            ).distinct()




        p = Paginator(queryset, 2)

        people = p.page(page)

        return people

    def get_context_data(self, **kwargs):
        """
        在默认的上下返回前端的基础上，增加上下文信息
        可以返回给前端更多的变量
        :param kwargs:
        :return:
        """

        type_all = TypeBook.objects.all()

        context = super(index, self).get_context_data(**kwargs)
        context['type_all'] = type_all

        try:
            context['is_type'] = int(self.is_type)
        except:
            context['is_type'] = ''

        try:
            context['is_status'] = int(self.is_status)
        except:
            pass

        context['search'] = self.search
        return context



class Addauthor(ListView):
    template_name = 'add_author.html'
    model = Author
    context_object_name = 'author_obj'

    def get_queryset(self):
        quryset = super(Addauthor, self).get_queryset()

        page = self.request.GET.get('page', 1)
        p = Paginator(quryset, 10)
        people = p.page(page)

        return people


    def get_context_data(self, **kwargs):
        author_form = AuthorForm()
        author_details_form = Author_DetailsForm()
        context = super(Addauthor, self).get_context_data()

        context['author_form'] = author_form
        context['author_details_form'] = Author_DetailsForm

        return context


    def post(self, request):
        ret = {'status':"","data": ""}
        author_form = AuthorForm(request.POST)
        if author_form.is_valid():
            author_data = author_form.cleaned_data
            author = Author()
            author.name = author_data['name']
            author.address = author_data['address']
            author.phone = author_data['phone']
            author.email = author_data['email']
            author.authorinfo = author_data['authorinfo']

            author.save()



            ret['status'] = "success"
            ret['data'] = '作者添加成功'


            return JsonResponse(ret)
        else:
            ret['data'] = author_form.errors

            return JsonResponse(ret)


class Author_Create_Details(View):
    """
    完善作者详情页功能
    """
    # def post(self, request):
    #     ret = {'status': "", "data": ""}
    #     print(request.POST)
    #     author_details_form = Author_DetailsForm(request.POST)
    #
    #     if author_details_form.is_valid():
    #         details_data = author_details_form.cleaned_data
    #         details = Details()
    #
    #         details.authorinfo = details_data['authorinfo']
    #         # details.save()
    #
    #
    #
    #         # 关联我们当前这本书的详细信息
    #         author_obj = Author.objects.get(id=int(request.POST.get('author_id')))
    #         author_obj.authorinfo = details
    #         author_obj.save()
    #
    #         ret['status'] = 'success'
    #         ret['data'] = '图书信息完善成功'
    #         return  JsonResponse(ret)
    #
    #
    #
    #     else:
    #         ret['data'] = author_details_form.errors
    #
    #
    #         return JsonResponse(ret)
    def post(self, request):
        ret = {'status':"","data": ""}
        author_details_form = Author_DetailsForm(request.POST)

        if author_details_form.is_valid():
            author_data = author_details_form.cleaned_data
            author = Author()
            author.authorinfo = author_data['authorinfo']




            author.save()



            ret['status'] = "success"
            ret['data'] = '作者添加成功'


            return JsonResponse(ret)
        else:
            ret['data'] = author_details_form.errors

            return JsonResponse(ret)


class Author_Del(View):
    """
    书籍删除功能
    """
    def post(self, request):
        ret = {'status': "success", "data": "删除成功"}

        author_id = request.POST.get('author_id')
        author_id = int(author_id)

        author_obj = Author.objects.get(id=author_id)
        author_obj.delete()

        return JsonResponse(ret)


class Addpublisher(ListView):
    template_name = 'add_publishe.html'
    model = Publisher
    context_object_name = 'publisher_obj'

    def get_queryset(self):
        quryset = super(Addpublisher, self).get_queryset()

        page = self.request.GET.get('page', 1)
        p = Paginator(quryset, 10)
        people = p.page(page)

        return people


    def get_context_data(self, **kwargs):
        publisher_form = PublisherForm()
        context = super(Addpublisher, self).get_context_data()

        context['publisher_form'] = publisher_form
        context['author_details_form'] = Author_DetailsForm

        return context


    def post(self, request):
        ret = {'status':"","data": ""}
        publisher_form = PublisherForm(request.POST)
        if publisher_form.is_valid():
            author_data = publisher_form.cleaned_data
            author = Publisher()
            author.name = author_data['name']
            author.address = author_data['address']


            author.save()



            ret['status'] = "success"
            ret['data'] = '作者添加成功'


            return JsonResponse(ret)
        else:
            ret['data'] = publisher_form.errors

            return JsonResponse(ret)

class Publisher_del(View):
    def post(self, request):
        ret = {'status': "success", "data": "删除成功"}
        print(request.POST)
        publisher_id = request.POST.get('publisher_id')

        publisher_id = int(publisher_id)


        author_obj = Publisher.objects.get(id=publisher_id)
        author_obj.delete()

        return JsonResponse(ret)


class Addtypebook(ListView):
    template_name = 'addtypebook.html'
    model = TypeBook
    context_object_name = 'type_obj'

    def get_queryset(self):
        quryset = super(Addtypebook, self).get_queryset()

        page = self.request.GET.get('page', 1)
        p = Paginator(quryset, 10)
        people = p.page(page)

        return people


    def get_context_data(self, **kwargs):
        author_form = Book_type()

        context = super(Addtypebook, self).get_context_data()

        context['author_form'] = author_form
        context['author_details_form'] = Author_DetailsForm

        return context


    def post(self, request):
        ret = {'status':"","data": ""}
        author_form = Book_type(request.POST)
        if author_form.is_valid():
            author_data = author_form.cleaned_data
            author = TypeBook()
            author.type_book = author_data['type_book']


            author.save()



            ret['status'] = "success"
            ret['data'] = '作者添加成功'


            return JsonResponse(ret)
        else:
            ret['data'] = author_form.errors

            return JsonResponse(ret)


class TypeBook_del(View):
    def post(self, request):
        ret = {'status': "success", "data": "删除成功"}
        print(request.POST)

        type_id = request.POST.get('type_id')
        type_id = int(type_id)

        author_obj = TypeBook.objects.get(id=type_id)
        author_obj.delete()

        return JsonResponse(ret)

