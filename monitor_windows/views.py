from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import subprocess
import json
import time

# Vista para mostrar la lista de procesos
def lista_procesos(request):
    start_time = time.time()
    result = subprocess.run(['powershell', 'Get-Process | Select-Object Name, Id, @{Name="State"; Expression={if ($_.HasExited) {"exited"} else {"running"}}} | ConvertTo-Json'], capture_output=True, text=True)
    procesos = json.loads(result.stdout)
    end_time = time.time()
    print(f"Process list retrieved and converted to JSON in {end_time - start_time} seconds")
    return render(request, 'monitor_windows/lista_procesos.html', {'procesos': procesos})

# Vista para terminar un proceso seleccionado
def terminar_proceso(request, pid):
    if request.method == 'POST':
        try:
            subprocess.run(['powershell', f'Stop-Process -Id {pid}'], check=True)
        except subprocess.CalledProcessError:
            # Manejo de error si el proceso ya no existe
            print(f"El proceso con PID {pid} no existe.")
    return redirect('lista_procesos')
