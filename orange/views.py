from django.shortcuts import render
from django.http import HttpResponse
import json

def test(request):
    num = request.POST.get('num')
    
    if num == '1':
        json_filename = "Fichier_Conf_1.json"
    elif num == '2':
        json_filename = "Fichier_Conf_1.json"
    elif num == '3':
        json_filename = "Fichier_Conf_1.json"
    elif num == '4':
        json_filename = "Fichier_Conf_4.json"
    elif num == '5':
        json_filename = "Fichier_Conf_5.json"
    else:
        # Handle other cases or raise an error
        json_filename = None
    
    if request.method == 'POST' and 'sub' in request.POST and json_filename:
        version = request.POST.get('version')
        name = request.POST.get('nsdName')
        nsdversion = request.POST.get('nsdVersion')
        nsddesc = request.POST.get('nsdDescription')
        softwaremin = request.POST.get('softwareMin')
        
        with open(f"orange/static/{json_filename}", "r") as file:
            data = json.load(file)
            i = 0
            inp = 0

            num = int(num)
            objects = data['objects']
            for object in objects:
                if data['objects'][i]['type']['value'] == "vnf" and num > 0:
                    vnfname = request.POST.get('name'+str(inp))
                    data['objects'][i]['name']['value'] = vnfname
                    memory = request.POST.get('memory'+str(inp))
                    data['objects'][i]['memory']['value'] = memory
                    cpu = request.POST.get('cpu'+str(inp))
                    data['objects'][i]['nof-vcpus']['value'] = cpu
                    url = data['objects'][i]['disks']['items'][0]['location']['value']
                    url = "https://10.253.56.133/"+url.rsplit('/', 1)[-1]
                    data['objects'][i]['disks']['items'][0]['location']['value'] = url
                    
                    #update persistance id
                    data['objects'][i]['persistence-id']['value'] = vnfname+"_3int"
                    
                    #collect Cloud-init paths and Cloud-init contents
                    cloud_init_paths = []
                    cloud_init_contents = []
                    for c in range(4):
                        path = request.POST.get('Cloud-init-path' + str(c) + '-' + str(i))
                        content = request.POST.get('Cloud-init-content' + str(c) + '-' + str(i))
                        cloud_init_paths.append(path)
                        cloud_init_contents.append(content)
                    i+=1
                    num-=1
                    inp = int(inp)
                    inp+=1
                elif data['objects'][i]['type']['value'] != "vnf" and num > 0:
                    i+=1
                elif num == 0:
                    break
            data['version'] = version
            data['nsd']['properties']['name'] = name
            data['nsd']['version'] = nsdversion
            data['nsd']['properties']['description'] = nsddesc
            data['nsd']['properties']['software_min'] = softwaremin
            data['general']['id']['value'] = name + "_3int"
        
        with open(f"orange/static/{json_filename}", "w") as file:
            json.dump(data, file, indent=4)
        
        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{json_filename}"'
        
        with open(f"orange/static/{json_filename}", "rb") as f:
            response.write(f.read())
        
        return response
    
    return render(request, "test.html")


def vnfconfig(request):
    #test to know witch file we will open
    i=0
    with open("orange/static/Fichier_Conf_1.json","r") as file:
        data = json.load(file)
    if request.method == 'POST':
        vnfname = request.POST.get('name${i}')
        nsdversion = request.POST.get('nsdVersion')
        nsddesc = request.POST.get('nsdDescription')
        softwaremin = request.POST.get('softwareMin')
        
        with open("orange/static/Fichier_Conf_1.json","w") as file:
            data['objects'][i]['name']['value'] = vnfname
            data['nsd']['version'] = nsdversion
            data['nsd']['properties']['description'] = nsddesc
            data['nsd']['properties']['software_min'] = softwaremin
    return render(request,"test.html")

'''
**********objects[type==vnf].name.value ==> VNF Name

**********objects[type==vnf].persistence-id.value ==> <VNF_Name>_3int

**********objects[type==vnf].memory.value ==> VNF memory (en GiB)

**********objects[type==vnf].nof-vcpus.value ==> VNF CPUs

**********objects[type==vnf].disks.items[0].location.value ===> "https://10.253.56.133/<VNF File>"

objects[type==vnf].cpu-pinning ===> à poser la questionb à Imane

objects[type==vnf].customization.pathnames.items[i].location ===> Cloud-init path i+1

objects[type==vnf].customization.pathnames.items[i].template-content ===> Cloud-init content i+1 (base64)             
'''