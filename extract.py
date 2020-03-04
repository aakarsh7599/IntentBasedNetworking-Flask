import json

with open('2level.json') as json_file:
    data = json.load(json_file)
    n=len(data['nmap details'])
    links=[]
    nodes=[]
    routersList={}
    for i in range(n):
        for ip in data['nmap details'][i]['scan']:
            if data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Interface'].startswith('r'):
                router=data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Interface'][:2]
                if router not in routersList.keys():
                    routersList[router]=[]
                    nodes.append({"name":router,"id":"router"})
                routersList[router].append(ip)
            elif data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Interface'].startswith('h'):
    	        host=data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Interface'][:2]
    	        nodes.append({"name":host,"id":"host"})
    #print(routersList)
    #print(nodes)
    nodeips={}
    for i in range(n):
        for ip in data['nmap details'][i]['scan']:
            node=data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Interface'][:2]
            nodeips[ip]=node
    count=0
    routers=[]
    for i in range(n):
        for ip in data['nmap details'][i]['scan']:
            ipv4_length=len(data['nmap details'][i]['scan'][ip]['Routing']['ipv4'])
            router=data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Interface'][:2]
            for j in range(ipv4_length):
            	if data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Interface'].startswith('r') and data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][j]['Gateway'] == "0.0.0.0":
                    if router not in routers:
                        links.append({"source":router,"target":""})
            routers.append(router)

    #print(links)
    for i in range(n):
        for ip in data['nmap details'][i]['scan']:
        	ipv4_length1=len(data['nmap details'][i]['scan'][ip]['Routing']['ipv4'])
        	#for j in range(ipv4_length1):
        	if data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Destination'] == 'default':
        	    for x in range(len(links)):
        	    	ipaddress=nodeips[data['nmap details'][i]['scan'][ip]['Routing']['ipv4'][0]['Gateway']]
        	    	if links[x]['source']==ipaddress and links[x]['target']=="":
        	    		links[x]['target']=nodeips[ip]
        	    		break
    length_links=len(links)
    del_links=[]
    for i in range(length_links):
    	if links[i]['target']=="": 
    		del_links.append(i)
    #print(del_links)
    #print(links)
    for i in range(len(del_links)):
        x=del_links[i]
        del links[x-i]

    #print(nodeips)
    node_indexes={}
    #for i in range(len(nodes)):

    print(nodes)
    print("******************")
    print(links)
    
