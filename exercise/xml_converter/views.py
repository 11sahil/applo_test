from django.http import JsonResponse
from django.shortcuts import render
import re

def upload_page(request):
    if request.method == 'POST':
        # TODO: Convert the submitted XML file into a JSON object and return to the user.
        file_data = request.FILES["file_uploaded"].read()
        file_data = file_data.decode("utf-8")
        file_data = file_data.split("\n")
        stk=[]
        for each_data in file_data:
            opening = re.findall("<[a-zA-z1-9]*>", each_data)
            closing = re.findall("</[a-zA-z1-9]*>", each_data)
            if opening and closing:
                text= re.findall(">[\w\W]*</", each_data)
                text =text[0].strip(">").strip("</")
                opening=opening[0].strip("<").strip(">")
                closing=closing[0].strip("<").strip(">")
                res = {opening:text}
                stk.append(res)
            elif opening:
                opening=opening[0].strip("<").strip(">")
                stk.append(opening)

            elif closing:
                closing=closing[0].strip("</").strip(">")
                pop=stk.pop()
                res={closing:[]}
                while pop!=closing:
                    res[closing].append(pop)
                    pop=stk.pop()
                lst = res[closing]
                res[closing] = lst[::-1]
                stk.append(res)
        print(stk[0])
        return JsonResponse(stk[0])

    return render(request, "upload_page.html")
