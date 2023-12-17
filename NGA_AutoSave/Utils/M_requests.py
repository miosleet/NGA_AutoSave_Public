import requests  
  
def get(url, params=None, **kwargs):  
    """  
    使用requests库发送GET请求，并根据重试次数进行重试。最多尝试进行5次访问  
  
    参数:  
    url (str): 请求的URL地址  
    params (dict, optional): 请求的参数，默认为None  
    retryCnt (int, optional): 重试次数，默认为0  
  
    返回:  
    requests.Response: 返回requests库的响应对象，如果请求失败则返回None  
  
    注意:  
    如果请求失败，且重试次数小于4次，会递归调用该函数并增加重试次数。  
    当重试次数达到4次时，将打印"访问失败，已达到最大重试次数"，并返回None。  
    """
    retryCnt = kwargs.pop('retryCnt', 0)  # 从kwargs中弹出retryCnt，默认为0  
    try:  
        response = requests.get(url, params=params, **kwargs)  
        response.raise_for_status()  # 如果状态不是200, 引发HTTPError异常  
        return response  
    except requests.exceptions.RequestException:  
        if retryCnt < 4:  
            retryCnt += 1  
            return get(url, params=params, **kwargs, retryCnt=retryCnt)  # 递归调用，增加retryCnt  
        else:  
            print("访问失败，已达到最大重试次数")  
            return None