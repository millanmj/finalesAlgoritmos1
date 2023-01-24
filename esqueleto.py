'''1) (DEBE RESOLVERSE EN PYTHON)
El área de Finanzas de la Clínica Esperanza nos solicita desarrollar un software que les permita entender la
situación financiera de cada uno de sus clientes.
 Para ello nos proveen 2 archivos con información respecto a sus clientes y a los comprobantes emitidos a
cada uno de ellos. Los clientes los tienen divididos en categorías (A/B/C). Respecto a los comprobantes vale aclarar
que las cobranzas se expresan en monto negativo y las facturas en positivo.
El formato de los archivos es el siguiente.
Clientes.csv: CUIT, Razón Social, Categoría de Cliente
Comprobantes.csv: CUIT, Fecha en formato AAAAMMDD, Tipo de Comprobante (Factura o Cobranza), Monto
(Se provee un ejemplo de cada archivo)
La solución deberá permitir:
1. Permitir el ingreso de nuevos movimientos para los clientes existentes (para simplificar)
2. Imprimir la deuda a una fecha para un determinado cliente. El usuario debe indicar el CUIL sobre el cual
quiere hacer el análisis.
3. Imprimir el listado de clientes con saldo a favor. Se debe indicar CUIL, Descripción y Monto.
4. Imprimir el reporte de Facturacion total por período ordenada por monto descendente. Se debe indicar:
Período (en formato AAAAMM) y monto.
5. Imprimir el reporte de Promedio de monto facturado según categoría de cliente. Se debe indicar: Categoría
y monto promedio.
Aclaración 1:Debe modularizarse en funciones.
Aclaración 2: Es obligatorio usar try except por lo menos en un lugar y justificar su uso
Aclaración 3: Es obligatorio el uso de una lista y un diccionario al menos
Aclaración 4: Debe existir un menú para poder llamar a las opciones a gusto del usuario'''



#pip install python-dotenv (instalen esto para poder usar la apikey)

import csv
import os




def menu()-> int:
    opciones: list[str] = [
        '1- Procesar archivo de denuncias',
        '2- Listar todas las infracciones dentro del centro de la ciudad',   
        '3- Listar los autos infraccionados con pedido de captura',
        '4- Listar autos infraccionados cercanos a los estadios',
        '5- Consultar infracciones por patente',
        '6- Mostrar grafico de denuncias por mes',
        '7- Ingrese 0 para salir'
    ]
    
    print('\n GESTOR DE DENUNCIAS \n')

    for item in opciones:
        print(item)
    opcion: int = int(input("\n Ingrese una opción:  ->  "))
    return opcion


def leerCSV(archivo: str) -> list:

    """
    Pre: Recibe del archivo csv a leer.
    Pos: Retorna una lista con los datos del archivo pasado.
    """
    
    try:
        datos:list = []
        with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
                csv_reader = csv.reader(archivo_csv, delimiter=',')
                next(csv_reader) 
                for linea in csv_reader:
                    datos.append(linea)
        
    except IOError: 
        print("procesando archivo....")   

    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    

    return datos




def imprimirCsv(datos: list) -> None:
    """
    Pre: Recibe una lista que se creó a partir de denuncias.csv
    Pos: Imprime de forma clara los datos de dicha lista.
    """
    for dato in datos:                    
        print("fecha y hora de la denuncia: ", dato[0])
        print("número: ", dato[1])
        print("Coordenadas latitud: ",dato[2])
        print("Coordenadas longitud: ", dato[3])
        print("ruta foto: ", dato[4])
        print("Texto de wsp: ", dato[5])
        print("ruta audio: ", dato[6])
        print("------------------------------------------")  


def procesarDenuncia(dato: list) -> list:
    """
    Pre: Recibe una lista con los datos de denuncias.csv
    Pos: Retorna una lista con los datos procesados.
    """
    lista:list = []
    timestamp: str = dato[0]
    telefono: str = dato[1]    
            
    ubicacion= obtenerDireccion(dato[2], dato[3])#consulta la api

    direccion: str = ubicacion[0]
    localidad: str = ubicacion[1] + ', ' +ubicacion[2]
    pais: str = ubicacion[3]

    patente: str = str(reconocer_patente(dato[4]))

    descripcion_en_txt: str = dato[5]
    descripcion_del_audio: str = convertirVozATexto(dato[6])

    lista.append(timestamp)
    lista.append(telefono)
    lista.append(direccion)
    lista.append(localidad)
    lista.append(pais)
    lista.append(patente)
    lista.append(descripcion_en_txt)
    lista.append(descripcion_del_audio)

    return lista


def crearCsv(datos: list) -> None:
    """
    Pre: Recibe una lista con los datos de denuncias.csv
    Pos: Crea el csv pedido en el punto 2.
    """
    matriz: list = []
    nuevasDenuncias: list = []
    matriz:list = [["Timestamp", "Telefono", "Dirección", "Localidad", "Pais", "Patente", "Descripcion_en_txt",  "Descripcion_del_audio"]]
    
    denunciados =leerCSV('datosProcesados.csv')

    for denuncia in denunciados:
        matriz.append(denuncia)

    #Verifico si existe el archivos en datos procesados  
    for dato in datos: 
        existeDenuncia = compararDenuncia(dato[0], 'datosProcesados.csv')

        if(existeDenuncia == False ):
            nuevasDenuncias.append(procesarDenuncia(dato))
    
    for fila in nuevasDenuncias:
        matriz.append(fila)

    try: 
        with open('datosProcesados.csv', 'w', newline='', encoding="UTF-8") as archivo_csv:
            csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)      
            csv_writer.writerows(matriz)
    
    except IOError: 
        
        print("No se encontró el archivo")   
    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    




    # for n in listaDeRobados:
    #   for key,value in formulario_robados.items():
    #     if n == key:
    #         print("----------------------------------------------")         
    #         print("Patente: {}".format(key))
    #         print("Ubicación del vehículo: {}".format(value[1]))
    #         print("Localidad: {}".format(value[2]))
    #         fecha = datetime.fromtimestamp(float(value[0]))#pasar de timestamp a fecha
    #         print("Fecha y hora de la denuncia: {}".format(fecha))           
    #         print("----------------------------------------------")
    #         autosRobados.append([value[1],value[2],fecha,key])

 



def main() -> None:

    lista: list =[]
    robados: list = []
    lista = leerCSV('Denuncias.csv')   

    opcion: int= 1
    
    while(opcion!= 0):
        
        opcion= menu()

        if (opcion == 1):
            print('opcion1')

            
        elif (opcion == 2):     
            print('opcion1')

           
        else: print('opcion3')


main()

