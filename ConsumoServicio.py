from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport
import logging.config
import datetime
import Parse_Document

# logging para que se imprima la informacion de los mensajes en la capa de transporte
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})


def correct_document(document):

    subs1 = '<SOAP-ENV:Envelope'
    subs2 = '</SOAP-ENV:Envelope>'
    index_sub2 = len(subs2)
    index1 = document.index(subs1)
    doc_len = len(document)
    res = document.replace(document[:index1], '')
    index2 = res.index(subs2)+index_sub2
    res2 = res.replace(res[index2:doc_len], '')

    return res2

def consumo_servicio():
    # Se envia la url y las credenciales como parametro para crear el cliente del servicio
    wsd = 'https://facturaelectronica.dian.gov.co/operacion/B2BIntegrationEngine/FacturaElectronica/consultaDocumentos.wsdl'
    transport = Transport(timeout=10)
    user = '5ac5e351-ed30-4e8c-90ff-d56d1ba91dbe'
    passwd = '7ea182d7fe1b9359812828166500793077c6d6f16ded5f8516159bc1b9fdf7e7'
    client = Client(wsdl=wsd,
                    wsse=UsernameToken(user, passwd),
                    transport=transport)

    # Se declara la fabrica para que el WS reciba los datos correctamente

    with open('info_facturas.txt', 'r') as info_facturas:
        for line in info_facturas.readlines():
            line_temp = line.split(",")
            strformat = "%Y-%m-%dT%H:%M:%S"
            id_fac = line_temp[0]
            fecha_fac = datetime.datetime.strptime(line_temp[1], strformat)
            nit_fac = line_temp[2]
            cufe_fac = line_temp[3].rstrip()
            factory = client.type_factory('ns0')

            date = fecha_fac
            tipoDoc = factory.TipoDocumenotoType('1')
            num_doc = factory.NumeroDocumentoType(id_fac)
            nit = factory.NitType(nit_fac)
            id_software = factory.IdentificadorSoftwareType('5ac5e351-ed30-4e8c-90ff-d56d1ba91dbe')
            cufe = factory.CufeType(cufe_fac)



            # Se configura el cliente para consumir el servicio
            with client.settings(strict=False, xml_huge_tree=False, raw_response=True):
                operation = client.service.ConsultaResultadoValidacionDocumentos(tipoDoc, num_doc, nit, date, id_software, cufe)
                operation_code = operation
                correct_res = correct_document(operation._content)
                with open('result.xml', 'w') as fileobj:
                    fileobj.write(str(correct_res))
                    fileobj.close()

            Parse_Document.parse_document(correct_res, operation_code.status_code, id_fac)

    info_facturas.close()
