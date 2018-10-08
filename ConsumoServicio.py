from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport
import pretend
import logging.config
import datetime

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


transport = Transport(timeout=10)
client = Client('https://facturaelectronica.dian.gov.co/operacion/B2BIntegrationEngine/FacturaElectronica/consultaDocumentos.wsdl',
                wsse=UsernameToken('5ac5e351-ed30-4e8c-90ff-d56d1ba91dbe', '7ea182d7fe1b9359812828166500793077c6d6f16ded5f8516159bc1b9fdf7e7'),
                transport=transport)

response = pretend.stub(
    status_code=200,
    headers={},
    content="""
        <!-- The response from the server -->
    """)
factory = client.type_factory('ns0')

date = datetime.datetime(2018, 9, 12, 23, 59, 00)

tipoDoc = factory.TipoDocumenotoType('1')
num_doc = factory.NumeroDocumentoType('E1306130024449')
nit = factory.NitType(860515812)

id_software = factory.IdentificadorSoftwareType('5ac5e351-ed30-4e8c-90ff-d56d1ba91dbe')
cufe = factory.CufeType('08eb0b17a357a7331abbedcc3a7b81d6bade4ad7')

print date

with client.settings(strict=False, xml_huge_tree=False):

    pack = client.service.ConsultaResultadoValidacionDocumentos(tipoDoc, num_doc, nit, date, id_software, cufe)



