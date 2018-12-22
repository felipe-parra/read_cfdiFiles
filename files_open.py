from xml.dom import minidom
import glob
import os
import pandas as pd
from pandas import ExcelWriter

def mes_consulta():
    mes = input("Ingresa mes a consultar, ej. 2018-01 \t")
    return mes

def open_file(file_name,mes_consulta):
    try:
        doc = minidom.parse(file_name)
    except:
        #print(file_name + "\tArchivo no compatible")
        return False

    doc = minidom.parse(file_name)
    relacionado_cfdi = ''
    datos_cfdi = doc.getElementsByTagName("cfdi:Comprobante")
    for dato in datos_cfdi:
        get_version = dato.getAttribute("Version")
        if(get_version):
            serie_Factura = dato.getAttribute("Serie")
            folio_Factura = dato.getAttribute("Folio")
            total_Factura = float(dato.getAttribute("Total"))
            str_total = "{:,.2f}".format(total_Factura)
            if(len(folio_Factura) <= 4):
                folio_Factura = folio_Factura + "\t"
            if(len(str_total) < 7):
                str_total = str_total + "\t"
            tipo_Factura = dato.getAttribute("TipoDeComprobante")
            if(tipo_Factura == "I"):
                tipo_Factura = "INGRESO"
                relacionado_cfdi = ""
            elif(tipo_Factura == "E"):
                tipo_Factura = "EGRESO"
                datos_relacion = doc.getElementsByTagName("cfdi:CfdiRelacionados")
                for datoR1 in datos_relacion:
                    datos_relaciones = doc.getElementsByTagName("cfdi:CfdiRelacionado")
                    for datoR2 in datos_relaciones:
                        relacionado_cfdi = datoR2.getAttribute("UUID")

        else:
            tipo_factura    = ""
            serie_Factura   = ""
            folio_Factura   = ""
            total_Factura   = ""
            str_total       = ""
            rfc_emisor      = ""
            uuid_cfdi       = ""
            fecha_timbrado  = ""
            relacionado_cfdi = ""
            return False

    datos_emisor = doc.getElementsByTagName("cfdi:Emisor")
    for dato in datos_emisor:
        rfc_emisor      = dato.getAttribute("Rfc")
        nombre_emisor   = dato.getAttribute("Nombre")
        #print(rfc_emisor)


    datos_receptor = doc.getElementsByTagName("cfdi:Receptor")
    for dato in datos_receptor:
        rfc_receptor    = dato.getAttribute("Rfc")
        nombre_receptor = dato.getAttribute("Nombre")

    datos_Complementos = doc.getElementsByTagName("cfdi:Complemento")
    for dato in datos_Complementos:
        datos_Timbrado = dato.getElementsByTagName("tfd:TimbreFiscalDigital")
        for datoTimbrado in datos_Timbrado:
            uuid_cfdi       = datoTimbrado.getAttribute("UUID")
            fecha_timbrado  = datoTimbrado.getAttribute("FechaTimbrado")

    diccionario_valido = {'Receptor': rfc_receptor,'RFC':rfc_emisor, 'Tipo':tipo_Factura , 'Folio': serie_Factura + folio_Factura, 'Total': str_total, 'Fecha':fecha_timbrado, 'UUID':uuid_cfdi}
    if(fecha_timbrado[0:7] == mes_consulta):
        print(rfc_receptor + "\t" + rfc_emisor + "\t" + tipo_Factura +"\t" +serie_Factura + folio_Factura + "\t" + str_total + "\t" + fecha_timbrado + "\t" + uuid_cfdi + "\t"+ relacionado_cfdi)



print("*" * 115)
def os_operations():
    x = os.getcwdb()
    os.chdir("../")
    print(x)


def direccion_consulta():
    direccion = None
    while not direccion:
        direccion = input("Ingresa direccion a consultar, ej. /Downloads/folder \t")
        try:
            if direccion[-1] == '/':
                return direccion
            else:
                return direccion + '/'
        except Exception as e:
            return '/'



if __name__ == '__main__':
    valor_mes = mes_consulta()
    valor_direccion = direccion_consulta()
    contador = 0
    archivos = glob.glob("{}*.xml".format(valor_direccion))
    #open_file(archivos[6])
    for i in archivos:
        contador += 1
        open_file(i,valor_mes)
    print("Numero de Archivos consultados:\t", contador)
