
from django import forms
# 定义组件和样式
from django.forms import widgets

from .models import TypeBook, Publisher, Author


class BookForm(forms.Form):
    """
    图书添加表单
    """
    name = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'bookname', "placeholder": "书名"}
        )
    )

    publish_year = forms.DateField(
        widget=widgets.DateInput(
            attrs={"placeholder": "出版日期: 2017-1-1", "class": "form-control", "id": "publish_year"}
        )
    )
    publish_add = forms.DateField(
        widget=widgets.DateInput(
            attrs={"placeholder": "添加日期: 2017-1-1", "class": "form-control", "id": "publish_add"}
        )
    )

    price = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "价格", "class": 'form-control', "id": "price"}
        )
    )

    stocks = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "库存", "class": 'form-control', "id": "stocks"}
        )
    )

    author = forms.MultipleChoiceField(
        choices=Author.objects.all().values_list('id', 'name'),
        widget=widgets.SelectMultiple(
            attrs={"id": "demo-cs-multiselect"}
        )
    )

    status = forms.ChoiceField(
        choices=[(1, "出版"), (0, '未出版')],
        widget=widgets.Select(
            attrs={"class": "magic-select", "type": "select", "id": 'status', }
        )

    )

    type = forms.ChoiceField(
        choices=TypeBook.objects.all().values_list('id', 'type_book'),
        widget=widgets.Select(
            attrs={"class": "selectpicker", "data-live-search": "true", "data-width": "100%", "id": "type", }
        )
    )

    publisher = forms.ChoiceField(
        choices=Publisher.objects.all().values_list('id', 'name'),
        widget=widgets.Select(
            attrs={"class": "selectpicker", "data-live-search": "true", "data-width": "100%", "id": "publisher", }
        )
    )


class DetailsForm(forms.Form):
    """
    图书详情表单
    """
    chapter = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "章节", "class": "form-control", 'id': 'chapter',}
        )
    )

    pages = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "页数", "class": "form-control", 'id': 'pages', }
        )
    )

    words = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "字数", "class": "form-control", 'id': 'words', }
        )
    )

    contentinfo = forms.CharField(
        widget=widgets.Textarea(
            attrs={"rows": 8, "class": 'form-control', "id": "demo-textarea-input-1", 'placeholder': '内容简介'}
        )
    )

    catalog = forms.CharField(
        widget=widgets.Textarea(
            attrs={"rows": 8, "class": 'form-control', "id": "demo-textarea-input-2", 'placeholder': '目录'}
        )
    )

    logo = forms.ImageField(
        required=False,
        widget=widgets.FileInput(
            attrs={"id": "logo_file", "class": 'fileinput-new btn btn-primary btn-file'}
        )
    )


class AuthorForm(forms.Form):
    """
    作者添加表单
    """
    name = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'authorname', "placeholder": "作者名"}
        )
    )
    address = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'address', "placeholder": "作者地址"}
        )
    )
    phone = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'phone', "placeholder": "作者联系方式"}
        )
    )
    email = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'email', "placeholder": "作者邮箱"}
        )
    )
    authorinfo = forms.CharField(
        widget=widgets.Textarea(
            attrs={"rows": 8, "class": 'form-control', "id": "authorinfo", 'placeholder': '作者简介'}
        )
    )


class Author_DetailsForm(forms.Form):
    """
    作者详情表单
    """


    authorinfo = forms.CharField(
        widget=widgets.Textarea(
            attrs={"rows": 8, "class": 'form-control', "id": "authorinfo", 'placeholder': '作者简介'}
        )
    )


class PublisherForm(forms.Form):
    """
    作者添加表单
    """
    name = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'publisher_name', "placeholder": "出版社名"}
        )
    )
    address = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'publisher_address', "placeholder": "出版社地址"}
        )
    )


class Book_type(forms.Form):
    type_book = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "id": 'book_type', "placeholder": "图书类型"}
        )
    )
