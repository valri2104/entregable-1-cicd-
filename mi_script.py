# mi_script.py
import platform
import datetime

AUTOR = "Valeria Cardona Urrea"  # Nombres completos del saludo y del README, en el mismo orden; para parejas usa "Nombre 1 | Nombre 2".

def main():
    print(f"Autor: {AUTOR}")
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Fecha y hora desde Python: {datetime.datetime.now()}")

if __name__ == "__main__":
    main()
