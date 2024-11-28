
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import subprocess
import json
import time
import platform

# Vista para mostrar la lista de procesos
def lista_procesos(request):
    start_time = time.time()
    if platform.system() == 'Windows':
        result = subprocess.run(['powershell', 'Get-Process | Select-Object Name, Id, @{Name="State"; Expression={if ($_.HasExited) {"exited"} else {"running"}}} | ConvertTo-Json'], capture_output=True, text=True)
        procesos = json.loads(result.stdout)
    else:
        result = subprocess.run(['ps', '-eo', 'pid,comm,state', '--no-headers', '--sort=-%mem'], capture_output=True, text=True)
        procesos = []
        for line in result.stdout.splitlines():
            pid, name, state = line.split(None, 2)
            procesos.append({'Id': pid, 'Name': name, 'State': 'running' if state == 'R' else 'exited'})
    end_time = time.time()
    print(f"Process list retrieved and converted to JSON in {end_time - start_time} seconds")
    return render(request, 'monitor/lista_procesos.html', {'procesos': procesos})

# Vista para terminar un proceso seleccionado
def terminar_proceso(request, pid):
    if request.method == 'POST':
        try:
            if platform.system() == 'Windows':
                subprocess.run(['powershell', f'Stop-Process -Id {pid}'], check=True)
            else:
                subprocess.run(['kill', '-9', str(pid)], check=True)
        except subprocess.CalledProcessError:
            print(f"El proceso con PID {pid} no existe.")
    return redirect('lista_procesos')