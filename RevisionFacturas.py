import ConsumoServicio
import Parse_Invoice
import ExtraccionXml


ExtraccionXml.extraer_factura()
Parse_Invoice.get_facturas()
ConsumoServicio.consumo_servicio()