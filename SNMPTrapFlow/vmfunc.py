import jsoncommon
import base64
import json
import ipaddress
import traceback


class VmFunc(object):
    
    vm_names = []
    vm_uuids = []
    vm_ips   = []
    vm_macs  = {}

    pc_user = "admin"
    pc_password = "Password"
    pc_ip = "XXX.XXX.XXX.XXX"


    def vmUpdate(self,uuid,payload):

        jsonfunc = jsoncommon.JsonCommon()

        url = "https://%s:9440/api/nutanix/v3/vms/%s" % (VmFunc.pc_ip,uuid)
        payload = payload.encode("utf-8")
        print("=== Quarantineカテゴリを送信 ===");

        return jsonfunc.put_restapitojson(url,VmFunc.pc_user,VmFunc.pc_password,payload)

        


    def getVmDetail(self,uuid):

        jsonfunc = jsoncommon.JsonCommon()

        url = "https://%s:9440/api/nutanix/v3/vms/%s" % (VmFunc.pc_ip,uuid)

        response = jsonfunc.get_restapitojson(url,VmFunc.pc_user,VmFunc.pc_password)
        return json.loads(response)



    def getVMList(self):
        
        #処理
        jsonfunc = jsoncommon.JsonCommon()



        flg = False
        cnt = 0

        print("=== 該当の仮想マシンを検索中 ===");
        
        url = "https://%s:9440/PrismGateway/services/rest/v1/vms/" % (VmFunc.pc_ip)

        response = jsonfunc.get_restapitojson(url,VmFunc.pc_user,VmFunc.pc_password)

        ret = type(response)
        if( ret is bool ):
            exit
        
        json_obj = json.loads(response)
        json_vm_datail = json_obj["entities"]

        for i in json_vm_datail:
            flg = False                    
            VmFunc.vm_names.append(i["vmName"])
            VmFunc.vm_uuids.append(i["uuid"])

            if( False ):
                if( len(i["ipAddresses"]) > 0 ):
                    #Listで複数ある
                    for j in i["ipAddresses"]:

                        if not "169.254" in j:
                            try:
                                ipaddress.IPv6Address(j)
                            
                                #IPv6は対象外のため追加から外す
                                if(flg):
                                    flg = True
                                else:
                                    VmFunc.vm_ips.append("")
                                    flg = True

                            except Exception as e:
                                #IPv6ではない

                                if(flg):
                                    VmFunc.vm_ips[len(VmFunc.vm_ips)-1] = j
                                    flg = True
                                else:
                                    VmFunc.vm_ips.append(j)
                                    flg = True
                        else:
                            if not flg:
                                VmFunc.vm_ips.append(j)


                else:
                    VmFunc.vm_ips.append("")

                flg = False

            #MACを取得
            for j in i["virtualNicIds"]:
                VmFunc.vm_macs[j[-17:].replace(":","").upper().replace(" ","")] = cnt


            cnt+=1 #カウンタアップ

        return {"vm_names":VmFunc.vm_names,"vm_uuids":VmFunc.vm_uuids,"vm_ips":VmFunc.vm_ips}



