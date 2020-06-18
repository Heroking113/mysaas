# _*_ coding: utf-8 _*_
from collections import OrderedDict

from django.utils import six
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomResponse(Response):
    class RetConstant(object):
        CODE_SUCCESS = 200
        MSG_SUCCESS = "success"

    def __init__(self,
                 code=RetConstant.CODE_SUCCESS,
                 message=RetConstant.MSG_SUCCESS,
                 data={},
                 result=True, status=status.HTTP_200_OK,
                 template_name=None,
                 headers=None,
                 exception=False,
                 content_type='application/json'
                 ):
        super(Response, self).__init__(None, status=status)
        self._code = code
        self._message = message
        self._data = data
        self._result = result

        self.data = {"result": result, "code": code, "message": message, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def result(self):
        return self._result

    @message.setter
    def result(self, value):
        self._result = value


class CustomPagination(PageNumberPagination):
    page_size = 3
    max_page_size = 50
    page_query_param = "page"
    page_size_query_param = page_size

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ("result", True),
            ("code", 200),
            ("messsage", "success"),
            ('count', self.page.paginator.count),
            ("data", data)
        ]))
