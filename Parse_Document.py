import xml.etree.ElementTree as ET

doc_recibido ='{http://www.dian.gov.co/servicios/facturaelectronica/ConsultaDocumentos}DocumentoRecibido'
datos_basicos = '{http://www.dian.gov.co/servicios/facturaelectronica/ConsultaDocumentos}DatosBasicosDocumento'
desc_estado = '{http://www.dian.gov.co/servicios/facturaelectronica/ConsultaDocumentos}DescripcionEstado'
veri_func = '{http://www.dian.gov.co/servicios/facturaelectronica/ConsultaDocumentos}VerificacionFuncional'
veri_doc = '{http://www.dian.gov.co/servicios/facturaelectronica/ConsultaDocumentos}VerificacionDocumento'
cod_verif = '{http://www.dian.gov.co/servicios/facturaelectronica/ConsultaDocumentos}CodigoVeriFunc'
desc_verif_func = '{http://www.dian.gov.co/servicios/facturaelectronica/ConsultaDocumentos}DescripcionVeriFunc'


def parse_document(document, response, invoice):
    descripcion_estado = ''
    resultado_estado = ''
    if response == 200:
        tree = ET.fromstring(document)

        for child in tree[1][0].findall(doc_recibido):
            child2 = child.find(datos_basicos)
            descripcion_estado += child2.find(desc_estado).text

            verificacion_func = child.findall(veri_func)
            for childother in verificacion_func:
                for oth in childother.findall(veri_doc):
                    if 'Incorrecta' in oth[1].text:
                        resultado_estado += oth[1].text
    else:
        descripcion_estado = '315'
        resultado_estado = 'No se encontraron resultados en el servicio'

    with open('ResultadoConsumo.csv', 'w') as resultado:
        resultado.write(str(invoice)+","+str(descripcion_estado)+","+str(resultado_estado))
    resultado.close()
