from urllib.parse import urlencode
import scrapy
import scrapy.http


def Request(url: str, type: str, method: str, callback, params: dict = {}, headers: dict = {}, meta: dict = {}, *args, **kwargs):
    """
    根据传入参数构造请求

    :param url: 链接
    :param type: 请求类型
    :param method: 请求方式
    :param headers: 请求头
    :param params: 请求参数
    """
    # 检查参数
    if type not in ["api", "browser"]:
        raise TypeError("Request Type must be 'api' or 'browser'")
    if type == "api" and method not in ["get", "post", ...]:
        raise TypeError("Request Method must be 'get' or 'post'")

    cb_kwargs = kwargs.get("cb_kwargs", {})
    cookies = kwargs.get("cookies", {})
    dont_filter = kwargs.get("dont_filter", True)  # 默认不过滤

    # 获取请求参数
    query_params = params.get("query", {})
    json_params = params.get("json", {})
    form_params = params.get("form", {})

    # 构造请求
    if type == "api":
        url = url + "?" + urlencode(query_params) if query_params else url

        if form_params:
            request = scrapy.http.FormRequest(
                url=url,
                method=method,
                headers=headers,
                cookies=cookies,
                formdata=form_params,
                meta=meta,
                callback=callback,
                cb_kwargs=cb_kwargs,
                dont_filter=dont_filter,
            )
            return request

        elif json_params:
            request = scrapy.http.JsonRequest(
                url=url,
                method=method,
                headers=headers,
                cookies=cookies,
                data=json_params,
                meta=meta,
                callback=callback,
                cb_kwargs=cb_kwargs,
                dont_filter=dont_filter,
            )
            return request

        else:
            request = scrapy.http.Request(
                url=url,
                method=method,
                headers=headers,
                cookies=cookies,
                meta=meta,
                callback=callback,
                cb_kwargs=cb_kwargs,
                dont_filter=dont_filter,
            )
            return request

    elif type == "browser":
        # TODO: 构造浏览器请求
        pass

    raise NotImplementedError("Request Method not implemented")
