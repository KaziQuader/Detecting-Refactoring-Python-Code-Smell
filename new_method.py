def method_1(reqResList, match, request, host, schemePort, scheme, port, getPostReq, forceBody, url, method, data, cookie, params, newline, lines, headers, index, line, value, key, errMsg, format, of, a, regular, expression, filtering, Exception, target):
    if not re.search(BURP_REQUEST_REGEX, content, re.I | re.S):
        if re.search(BURP_XML_HISTORY_REGEX, content, re.I | re.S):
            reqResList = []
            for match in re.finditer(BURP_XML_HISTORY_REGEX, content, re.I | re.S):
                port, request = match.groups()
                try:
                    request = decodeBase64(request, binary=False)
                except (binascii.Error, TypeError):
                    continue
                _ = re.search(r"%s:.+" % re.escape(HTTP_HEADER.HOST), request)
                if _:
                    host = _.group(0).strip()
                    if not re.search(r":\d+\Z", host):
                        request = request.replace(host, "%s:%d" % (host, int(port)))
                reqResList.append(request)
        else:
            reqResList = [content]
    else:
        reqResList = re.finditer(BURP_REQUEST_REGEX, content, re.I | re.S)

def method_2(reqResList, match, request, host, schemePort, scheme, port, getPostReq, forceBody, url, method, data, cookie, params, newline, lines, headers, index, line, value, key, errMsg, format, of, a, regular, expression, filtering, Exception, target):
        getPostReq = False
        forceBody = False
        url = None
        host = None
        method = None
        data = None
        cookie = None
        params = False
        newline = None
        lines = request.split('\n')
        headers = []

