from pymongo import MongoClient
import os
import datetime


def extraer_factura():
    client = MongoClient("localhost:27017")
    db = client['certifacturadb']
    db.authenticate('certifactura', 'certifactura', source='certifacturadb')
    collection = db['EvidenciaDigitalXml']
    print "conexion correcta"

    fechaInicial = datetime.datetime(int(2018), int(06), int(28), 0, 0, 0)
    fechaFinal = datetime.datetime(int(2018), int(07), int(01), 23, 59, 59)

    query = {"fechaExpedicion": {"$gte": fechaInicial, "$lt": fechaFinal}}


    documents = collection.find(query)
    cont = 0
    with open('nombrefacturas.txt', 'w') as write_facturas:
        for document in documents:
            write_facturas.write(document["_id"]+".xml"+"\n")

            path = os.path.join("/home/davidsalazar/Escritorio/truncado/base64", document['_id']+".xml")
            with open(path, 'w') as fileobj:
                fileobj.write(document['archivo'])
                print "file wrote "+document["_id"]
            fileobj.close()
            cont += 1
            print cont
    write_facturas.close()
    print "totalDocumentos"+str(cont)
    client.close()
