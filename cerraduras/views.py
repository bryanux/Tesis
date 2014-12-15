# Create your views here.
from audioop import reverse
from django.contrib.sessions import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from models import *


def usuario(request):


        try:
            print "1"
            if request.session['sesionUsuario'] is not None :
                print "2"
                persona = personal.objects.get(username = request.session['sesionUsuario'])
                print "3"
                puertas = cerraduras.objects.filter(id_personal = persona.id_personal)
                print "4"
                return render_to_response('usuarios.html', {"nombre":persona , "puertas":puertas})

            print "5"

        except:
            print "6"
            return HttpResponseRedirect('/cerrarSesion/')

        print "7"










def administrador(request):
    usuarios = personal.objects.filter(tipo='Usuario')
    return render_to_response('administrador.html', {"usuarios":usuarios})



def index(request):
    try:
        if request.session['sesionUsuario'] is not None :
            return HttpResponseRedirect('/usuario/')
    except:
        try:
            if request.session['sesionAdministrador'] is not None :
                return HttpResponseRedirect('/administrador/')
        except:
            return render_to_response('index.html')


def login(request):
    return render_to_response('login.html')




def verificarLogin(request):
    print "11111111"
    if request.method == 'POST':
        print "02222222"
        try:
            if request.session['sesionUsuario'] is not None :
                return HttpResponseRedirect('/usuario/')
                print "0"
            elif request.session['sesionAdministrador'] is not None :
                print "1"
                return HttpResponseRedirect('/administrador/')
        except:
            username=request.POST['username']
            passwd=request.POST['passwd']
            try: #ingresa administrador
                admin = personal.objects.get(username=username, clave=passwd, tipo='Administrador')
                #mivar = {"variable": username+" "+ passwd + "SI HAY eres ADMINISTRADOR"}
                request.session['sesionAdministrador']=admin.nombre
                print "2"
                return HttpResponseRedirect('/administrador/')

                #return render_to_response('mostrar.html', {"variable": username+" "+ passwd + "SI HAY eres ADMINISTRADOR"})
            except personal.DoesNotExist:
                try:#ingresa usuario o terrateniente
                    usuarionoDB = personal.objects.get(username=username, clave=passwd, tipo='Usuario')
                    request.session['sesionUsuario']=usuarionoDB.username
                    print "3"
                    return HttpResponseRedirect('/usuario/')

                except  personal.DoesNotExist: #credenciales incorrectas
                    return render_to_response('login.html' , {"error": "Usuario no encontrado"})#, {"variable": username+" "+ passwd + "NO HAY NADA"})
    else:
        return render_to_response('login.html')

    #return render_to_response('login.html')



def cerrarSesion(request):
    try:
        del request.session['sesionUsuario']
        return render_to_response('index.html', {"var":None})
    except:
        try:
            del request.session['sesionAdministrador']
            return render_to_response('index.html', {"var":None})
        except:
            return render_to_response('index.html', {"var":None})







def nuevoUsuario(request):
    return render_to_response('nuevoUsuario.html')


def ingresarUsuario(request):
    if request.POST:
        usuario=request.POST['username2']
        saberSiExiste = personal.objects.filter(username = usuario)
        cont = 0;
        for i in saberSiExiste:
            cont = cont + 1


        if cont>0:
            return render_to_response('nuevoUsuario.html',{"existe":"Nombre de usuario existente"})

        else:


            nombre=request.POST['nombre']
            apellido=request.POST['apellido']
            usuario=request.POST['username2']
            password=request.POST['passwd2']
            guardarRegistro =personal(nombre=nombre, apellido=apellido,username=usuario, clave= password, tipo='Usuario')
            guardarRegistro.save()
            lista = []
            try:
                l1 = request.POST['lab1']
                lista.append(l1)
            except:
                False

            try:
                l2 = request.POST['lab2']
                lista.append(l2)
            except:
                False

            try:
                l3 = request.POST['lab3']
                lista.append(l3)
            except:
                False

            try:
                l4 = request.POST['lab4']
                lista.append(l4)
            except:
                False

            try:
                l5 = request.POST['lab5']
                lista.append(l5)
            except:
                False

            try:
                l6 = request.POST['lab6']
                lista.append(l6)
            except:
                False

            try:
                telecomunicaciones = request.POST['telecomunicaciones']
                lista.append(telecomunicaciones)
            except:
                False

            try:
                mac = request.POST['mac']
                lista.append(mac)
            except:
                False

            try:
                direccion = request.POST['direccion']
                lista.append(direccion)
            except:
                False

            try:
                electronica = request.POST['electronica']
                lista.append(electronica)
            except:
                False

            try:
                ciditec = request.POST['ciditec']
                lista.append(ciditec)
            except:
                False

            try:
                administradorTecnico = request.POST['administradorTecnico']
                lista.append(administradorTecnico)
            except:
                False


            #extraerCodigo = personal.objects.values_list('id_personal',flat=True).filter(nombre=nombre,apellido=apellido,username=usuario, clave= password, tipo='Usuario')
            #obtenerId = personal.objects.get(id_personal=extraerCodigo)
            obtenerId = personal.objects.get(nombre=nombre,apellido=apellido,username=usuario, clave= password, tipo='Usuario')
            for i in lista:
                print i
                guardarPuerta = cerraduras(nombre=i, id_personal= obtenerId)
                guardarPuerta.save()

                #guardarPuerta =personal(nombre=i, po='Usuario')
            #guardarRegistro.save()

            #lab1 = 22, lab2 = 23, lab3 = 24, lab4 = 25, lab5 = 26, lab6 = 27, telecomunicaciones = 28
            #mac = 29, direccion = 30, electronica = 31, administradorTecnico = 32
            return HttpResponseRedirect('/administrador/')

    else:
        return render_to_response('/')



def usuarioEspecifico(request):

    if request.POST:
        id=request.POST['idUsuario']
        especifico = personal.objects.get(id_personal  = id)
        puertasEspecifico = cerraduras.objects.filter(id_personal = especifico)
        return render_to_response('usuarioEspecifico.html',{"id":especifico,"puertas":puertasEspecifico})


def editarUsuario(request):
    if request.POST:

        id=request.POST['id']
        nombre=request.POST['nombre']
        apellido=request.POST['apellido']
        usuario=request.POST['username3']
        password=request.POST['passwd3']
        guardarRegistro =personal(id_personal = id, nombre=nombre, apellido=apellido,username=usuario, clave= password, tipo='Usuario')
        guardarRegistro.save()
        registros = cerraduras.objects.filter(id_personal=id)
        registros.delete()

        lista = []
        try:
            l1 = request.POST['lab1']
            lista.append(l1)
        except:
            False

        try:
            l2 = request.POST['lab2']
            lista.append(l2)
        except:
            False

        try:
            l3 = request.POST['lab3']
            lista.append(l3)
        except:
            False

        try:
            l4 = request.POST['lab4']
            lista.append(l4)
        except:
            False

        try:
            l5 = request.POST['lab5']
            lista.append(l5)
        except:
            False

        try:
            l6 = request.POST['lab6']
            lista.append(l6)
        except:
            False

        try:
            telecomunicaciones = request.POST['telecomunicaciones']
            lista.append(telecomunicaciones)
        except:
            False

        try:
            mac = request.POST['mac']
            lista.append(mac)
        except:
            False

        try:
            direccion = request.POST['direccion']
            lista.append(direccion)
        except:
            False

        try:
            electronica = request.POST['electronica']
            lista.append(electronica)
        except:
            False

        try:
            ciditec = request.POST['ciditec']
            lista.append(ciditec)
        except:
            False

        try:
            administradorTecnico = request.POST['administradorTecnico']
            lista.append(administradorTecnico)
        except:
            False

        obtenerId = personal.objects.get(nombre=nombre,apellido=apellido,username=usuario, clave= password, tipo='Usuario')
        for i in lista:
            print i
            guardarPuerta = cerraduras(nombre=i, id_personal= obtenerId)
            guardarPuerta.save()

        return HttpResponseRedirect('/administrador/')

    else:
        return render_to_response('/')


def eliminarUsuario(request):
    if request.POST:
        id=request.POST['id']
        eliminarRegistro =personal(id_personal = id)
        eliminarRegistro.delete()
        return HttpResponseRedirect('/administrador/')
    else:
        return render_to_response('/')

def comprobarUsername(request):
    username=request.GET['username']
    existe = personal.objects.filter(username=username)
    cont = 0
    data = "NO EXISTE"
    for i in existe:
        cont = cont + 1

    if cont>0:
        data = "SI EXISTE"
    return HttpResponse(data)



def comprobarPasswords(request):
    pass1=request.GET['pass1']
    pass2=request.GET['pass2']
    existePass = personal.objects.filter(clave=pass1, tipo='Administrador')
    cont = 0
    data = 0
    for i in existePass:
        cont = cont + 1

    if cont>0:
        #MyModel.objects.filter(pk=some_value).update(field1='some value')
        actualizarPassword = personal.objects.filter(id_personal=1).update(clave=pass2)

        data = 1

    return HttpResponse(data)



def lab1(request):
    if request.method=='POST':
        return render_to_response('lab1.html')
    else:
        return HttpResponseRedirect('/')

def lab2(request):
    if request.method=='POST':
        return render_to_response('lab2.html')
    else:
        return HttpResponseRedirect('/')

def lab3(request):
    if request.method=='POST':
        return render_to_response('lab3.html')
    else:
        return HttpResponseRedirect('/')

def lab4(request):
    if request.method=='POST':
        return render_to_response('lab4.html')
    else:
        return HttpResponseRedirect('/')

def lab5(request):
    if request.method=='POST':
        return render_to_response('lab5.html')
    else:
        return HttpResponseRedirect('/')

def lab6(request):
    if request.method=='POST':
        return render_to_response('lab6.html')
    else:
        return HttpResponseRedirect('/')