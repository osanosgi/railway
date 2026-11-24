from django.shortcuts import render,redirect,get_object_or_404 #mensaje si error en el form
from django.http import JsonResponse
from datetime import datetime, timezone
from .mongo import registrar_auditoria # vista para mongo db

from .mongo import auditoria

#formulario creado
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

def prueba_mongo(request):
    resultado = auditoria.insert_one({
        "accion": "prueba_conexion",
        "descripcion": "Registro desde Django",
        "fecha": datetime.now(timezone.utc)
    })

    return JsonResponse({
        "mensaje": "Documento guardado en MongoDB",
        "id": str(resultado.inserted_id)
    })

def listar_productos(request):
    productos = Producto.objects.all()
    return render(
        request,
        "productos/listar.html",
        {"productos": productos},
    )



def crear_producto(request):
    if request.method == "POST":
        formulario = ProductoForm(request.POST)








        if formulario.is_valid():
            producto = formulario.save()

            try:
                registrar_auditoria(
                    accion="creado",
                    registro_id=producto.pk,
                    detalles={
                        "nombre": producto.nombre,
                        "precio": str(producto.precio),
                        "cantidad": producto.cantidad,
                        "estado": producto.estado,
                    },
                    usuario=(
                        request.user.username
                        if request.user.is_authenticated
                        else None
                    ),
                )

            except Exception:
                import logging
                logging.exception(
                    "El producto se guardó en MySQL, "
                    "pero falló la auditoría en MongoDB."
                )
                messages.warning(
                    request,
                    "El producto se guardó en MySQL, "
                    "pero falló el registro de auditoría."
                )
                return redirect("listar_productos")

            messages.success(
                request,
                "Producto creado y auditado correctamente."
            )
            return redirect("listar_productos")

    else:
        formulario = ProductoForm()

    return render(
        request,
        "productos/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Crear producto",
        },
    )


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        formulario = ProductoForm(
            request.POST,
            instance=producto
        )

        if formulario.is_valid():
            producto = formulario.save()

            try:
                registrar_auditoria(
                    accion="actualizado",
                    registro_id=producto.pk,
                    detalles={
                        "nombre": producto.nombre,
                        "precio": str(producto.precio),
                        "cantidad": producto.cantidad,
                        "estado": producto.estado,
                    },
                    usuario=(
                        request.user.username
                        if request.user.is_authenticated
                        else None
                    ),
                )

            except Exception:
                import logging
                logging.exception(
                    "El producto se actualizó en MySQL, "
                    "pero falló la auditoría en MongoDB."
                )
                messages.warning(
                    request,
                    "El producto se actualizó, "
                    "pero falló el registro de auditoría."
                )
                return redirect("listar_productos")

            messages.success(
                request,
                "Producto actualizado y auditado correctamente."
            )
            return redirect("listar_productos")

    else:
        formulario = ProductoForm(instance=producto)

    return render(
        request,
        "productos/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Editar producto",
        },
    )


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        datos_producto = {
            "nombre": producto.nombre,
            "precio": str(producto.precio),
            "cantidad": producto.cantidad,
            "estado": producto.estado,
        }

        try:
            registrar_auditoria(
                accion="eliminado",
                registro_id=producto.pk,
                detalles=datos_producto,
                usuario=(
                    request.user.username
                    if request.user.is_authenticated
                    else None
                ),
            )

        except Exception:
            import logging
            logging.exception(
                "Falló la auditoría en MongoDB. "
                "Se cancela la eliminación del producto."
            )
            messages.error(
                request,
                "No se eliminó el producto porque "
                "no se pudo registrar la auditoría."
            )
            return redirect("listar_productos")

        producto.delete()

        messages.success(
            request,
            "Producto eliminado y evento de auditoría registrado."
        )
        return redirect("listar_productos")

    return render(
        request,
        "productos/confirmar_eliminacion.html",
        {"producto": producto},
    )
