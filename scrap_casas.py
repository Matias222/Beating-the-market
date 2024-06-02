from betway import req_betway
from apuesta_total import req_apuesta_total
from dorado import req_dorado
from betano import req_betano

from escribir_csv import append_csv

def todo():

    arr=["at","dorado","betano","betway"]

    llamadas = [req_apuesta_total, req_dorado, req_betano, req_betway]

    for i in range(len(llamadas)):
        print("Llamando",arr[i])
        escribir=llamadas[i]()
        append_csv(arr[i],escribir)

todo()