import xml.etree.ElementTree as ET
import os

def get_documents():
    lista_facturas = []
    with open('nombrefacturas.txt', 'r') as nombresFacturas:
        for line in nombresFacturas.readlines():
            lista_facturas.append(line.strip())
    nombresFacturas.close()
    return lista_facturas


def get_facturas():
    facturas = get_documents()

    with open('info_facturas.txt', 'w') as info_facturas:
        for factura in facturas:
            path = os.path.join("/home/davidsalazar/Escritorio/truncado/base64", factura)
            with open(path, 'r') as nombre_factura:
                tree = ET.parse(nombre_factura)
                root = tree.getroot()

                id_fac = root.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID').text
                cufe_fac = root.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}UUID').text
                fecha = root.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate').text
                hora = root.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueTime').text
                fecha_fac = fecha+"T"+hora

                for supplier in root.findall('{http://www.dian.gov.co/contratos/facturaelectronica/v1}AccountingSupplierParty'):
                    for party in supplier.findall('{http://www.dian.gov.co/contratos/facturaelectronica/v1}Party'):
                        nit = party[0][0].text
                info_facturas.write(id_fac+","+fecha_fac+","+nit+","+cufe_fac+"\n")
            nombre_factura.close()
    info_facturas.close()

