"""Ejecuta los 4 ejercicios de la practica de Sistemas Difusos."""
import ejercicio1_variables
import ejercicio2_operadores
import ejercicio3_composicion
import ejercicio4_composicion_producto

if __name__ == "__main__":
    for modulo in (ejercicio1_variables, ejercicio2_operadores,
                   ejercicio3_composicion, ejercicio4_composicion_producto):
        modulo.main()
        print("\n" + "=" * 70 + "\n")
