
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

import base64
import json
import jsoncommon
import ipaddress
import traceback
import vmfunc

class Flow:
    """description of class"""
    description_oid = ""
    trend_val = ""
    msgval = []

    idx  = 0
    idx2 = 0

    #python snmp trap receiver

    snmpEngine = engine.SnmpEngine()

    TrapAgentAddress=''; #Trap listerner address
    Port=162;  #trap listerner port


    print("Nutanix Flow TrendMicro Apex One MicroSeg listening SNMP Trap on "+TrapAgentAddress+" , Port : " +str(Port));
    print('---------------------------------------------------------------------------------------');
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
    )

    #Configure community here
    config.addV1System(snmpEngine, 'my-area', 'public')

    def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
              varBinds, cbCtx):

        try:

            print("=== SNMP Trapを受信 ===");
            for name, val in varBinds:
                description_oid = name.prettyPrint()

                #TrendMicro ウイルス完成OID
                if( description_oid == '1.3.6.1.4.1.6101.141' ):
                    print("=== ウイルスバスターのトラップ情報 ===")
                    trend_val = val._value.decode("sjis")
                    print(trend_val)
                    msgval = trend_val.split(",")


                    #最新の仮想マシン情報を取得する
                    ans = vmfunc.VmFunc.getVMList("")

                    
                    #IPからIndexを探す
                    try:
                        idx = vmfunc.VmFunc.vm_macs[msgval[1].replace("-","").upper().replace(" ","")]

                    except Exception as e:
                        print("=== 該当のIPアドレスが存在しない（処理終了） ===")
                        break
                
                    
                    uuid = vmfunc.VmFunc.vm_uuids[idx]

                    json_obj = vmfunc.VmFunc.getVmDetail("",uuid)

                    print("=== 該当の仮想マシンの詳細情報を取得中 ===");

                    json_obj_seiton = {"spec": json_obj["spec"]}
                    json_obj_seiton.update({"metadata": json_obj["metadata"]})
                    json_obj_seiton.update({"api_version": json_obj["api_version"]})

                    json_obj_seiton["metadata"].update({"categories_mapping": { "Quarantine": [ "Default" ] }})
                    json_obj_seiton["metadata"].update({"use_categories_mapping": True})

                    spec_version = int(json_obj_seiton["metadata"]["spec_version"]) 

                    json_obj_seiton["metadata"].update({"spec_version": spec_version})
                
                    payload = json.dumps(json_obj_seiton)

                    response = vmfunc.VmFunc.vmUpdate("",uuid,payload)
                    
                    print("\r\n=== Prismからの結果 ===");
                    print(json.loads(response))


                #SNMP出力
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

        except Exception as e:
            print(e)
            

    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    snmpEngine.transportDispatcher.jobStarted(1)  

    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise

