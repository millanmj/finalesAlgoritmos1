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


#FUNCION PARA BORRAR (es para borrar)
def cls() -> None:
    command = 'clear'

    if os.name in ('nt', 'dos'):
        command = 'cls'

    os.system(command)

def menu()-> int:
    '''
    Pre: --
    Pos: Muestra el menu de opciones y devuelve la opción elegida por el usuario.
    '''
    esValida: bool = False
    opciones: list[str] = [
        '1- Ingresar nuevo movimiento para un Cliente',
        '2- Imprimir deuda a una fecha',   
        '3- Listar Clientes con saldo a favor',
        '4- Imprimir el reporte de Facturacion total por período',
        '5- Imprimir el reporte de Promedio de monto facturado según categoría de cliente',        

        '0- Ingrese 0 para salir'
    ]
    
    print('\n Finanzas de la Clínica Esperanza \n')

    for item in opciones:
        print(item)
    
    while(esValida == False):
        
        try:    
            opcion: int = int(input("\n Ingrese una opción:  ->  "))
            esValida = True
        except ValueError: 
            print('Por favor ingrese un número:')
    cls()                  
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
                next(csv_reader) #Para saltear el header
                for linea in csv_reader:
                    datos.append(linea)
        
    except IOError: 
        print("No se encontro el archivo")   

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

   
    
    for fila in nuevasDenuncias:
        matriz.append(fila)

    try: 
        with open('Clientes.csv', 'a', newline='', encoding="UTF-8") as archivo_csv:
            csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)      
            csv_writer.writerows(matriz)
    
    except IOError: 
        
        print("No se encontró el archivo")   
    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    


def agregarRegistro(nombreArchivo: str, registro: list) -> None:
    #agregamos el registro al final

    try: 
        with open(nombreArchivo, 'a', newline='', encoding="UTF-8") as archivo_csv:
            csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
            # csv_writer.writerows(['\n'])
            csv_writer.writerows(registro)
    
    except IOError:         
        print("No se encontró el archivo") 

    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde") 


def nuevoComprobante(nombreArchivo: str = 'Comprobantes.csv')-> bool:
    '''
    #Cuit,Fecha,Tipo de Comprobante,Monto
    222222222,20220601,Factura,12334
    '''
    registro: list = []
    esValida: bool = False
    while(esValida == False):
        try:
            cuit: int = int(input("\n Ingrese el CUIT:  ->  "))
            fecha: int = int(input("\n Ingrese una Fecha en formato AAAAMMDD:  ->  "))
            tipo: str = (input("\n Ingrese un tipo de comprobante:  ->  "))
            monto: int = int(input("\n Ingrese un monto:  ->  "))
            
            print('Los datos fueron ingresados correctamente')
            registro.append([cuit,fecha,tipo,monto])    
            esValida = True
        
        except ValueError:
            print('Por favor ingrese los datos correctamente')

    #ahora hay que grabar los datos en el csv
    agregarRegistro(nombreArchivo, registro)

    






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
    registroOk = False
    opcion: int= 1
    
    while(opcion!= 0):
        
        opcion= menu()

        if (opcion == 1):
            print('1- Ingresar nuevo movimiento para un Cliente')
            
            registroOk = nuevoComprobante()
            
            if (registroOk == True):
                print('El movimiento ha sido agregado correctamente')
            else: print('Por favor vuelva a ingresar el comprobante')

            

        elif (opcion == 2):     
            print('2-Imprimir deuda a una fecha')
            
        elif (opcion == 3):
            print('3- Listar Clientes con saldo a favor')
            
        elif (opcion == 4):     
            print('4- Imprimir el reporte de Facturacion total por período')
        
        elif (opcion == 5):
            print('5- Imprimir el reporte de Promedio de monto facturado según categoría de cliente')
        
        else: print('Por favor ingrese una opción valida')


main()

