from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView, 
    ListCreateAPIView, 
    RetrieveAPIView, 
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import BasePermission
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password

from users.models import CustomUser, Client, Worker


from users.serializers import (
    UserSerializer, 
     
    #CreateNewClientSerializer,
    ClientSerializer, 
    ClientAllSerializer,
    #CreateClientSerializer,
    #UpdateClientSerializer,
    WorkerSerializer,
    WorkerSingleSerializer,
    UserLoginSerializer,
    SuperLoginSerializer,
    RequestPasswordReset,
    PasswordReset,
    #CreateNewWorkerSerializer,
)
from rest_framework.views import APIView 
from rest_framework.response import Response

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token



from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

""" ===================================================
Las siguientes clases verifican si quien consulta una ruta
tiene el cargo para poder hacer dicha consulta.
"""
"""
class AllowAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            quey = Worker.objects.filter(user=request.user.id).values('user_type')
            return bool(quey[0]['user_type']==1)            
        else:
            return False

class AllowManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            quey = Worker.objects.filter(user=request.user.id).values('user_type')
            return bool(quey[0]['user_type']==2)            
        else:
            return False

class AllowOperator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            quey = Worker.objects.filter(user=request.user.id).values('user_type')
            return bool(quey[0]['user_type']==3)            
        else:
            return False
"""
# ============== Metodo del login =================
"""
class Login(APIView):
  def post(self,request):
    id_user = request.data.get('id_user',None)
    password = request.data.get('password',None)
    if id_user and password:
        user_querysets = Worker.objects.filter(user__email__iexact= id_user ).values('id','user','user__id_user', 'user__is_active',  'user__password', 'user_type')  
        if (user_querysets.exists() and  user_querysets[0]['user__is_active']) :
            user= user_querysets[0]
            if(check_password(password, user['user__password'])):
                user.pop('user__password')
                user.pop('user__is_active')
                userC = CustomUser.objects.filter(email__iexact=id_user)
                token, created  = Token.objects.get_or_create(user=userC[0])
                return Response({"message": "Login exitoso",  "code": 200, "token": token.key, "data":  user})
            else:
                message= "Contraseña incorrecta"
                return Response({"message": message , "code": 204, 'data': {}} )     

        else:
            message = "El id proporcionado no existe o el usuario no está activo"
            return Response({"message": message , "code": 204, 'data': {}} )
    else:
        message = "No ha proporciando datos validos"
        return Response({"message": message , "code": 204, 'data': {}})

"""
class Login(APIView):
    serializer_class = UserLoginSerializer
    def post(self,request):

        copy_data = request.data.copy()
        copy_data['type'] = request.path.split("/")[-3]
        if (request.data.get('type')!=None):
            copy_data['social'] = request.data['type']
 
        serializer = UserLoginSerializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': ClientAllSerializer(user).data if copy_data['type']=='client' else WorkerSerializer(user).data ,
            'access_token': token
        }
        return Response(data)

class LoginSuper(APIView):
    serializer_class = SuperLoginSerializer
    def post(self,request):
        serializer = SuperLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserSerializer(user).data,
            'access_token': token
        }
        return Response(data)

class RequestPasswordResetView(APIView):
    serializer_class = RequestPasswordReset
    def post(self,request):
        serializer = RequestPasswordReset(data=request.data)
        serializer.is_valid(raise_exception=True)
        idlink = serializer.save()


        try:

            html_part = MIMEMultipart(_subtype='related')
            body = '''
                <h2>Hola</h2>
                <p><b>APRECIADO USUARIO</b></p>
                <div style="padding-top: 20px;border-top: 5px solid crimson;">
                <div style="clear: left; float: left;margin-right: 1em; ">
                    <img width="70px" src="https://1.bp.blogspot.com/-ebhZaGmzGqY/X8mcxbPJKRI/AAAAAAAAIrQ/gHtVWVGDkEUnRsjfcd4xvkTOzLo2uh3EgCLcBGAsYHQ/s0/reset-password.png" />
                </div>
                </div>    
                Usted recientemente solicito el cambio de contraseña para su cuenta.<br/>
                A continuación aparece un botón ROJO para hacer el cambio, una vez
                haga click sobre el botón, podrás continuar con el cambio de contraseña, 
                si usted no ha realizado dicha solicitud, por favor haga caso omiso a este mensaje.
                <br/><br/><br/>
                ''' + request.get_host() + "/reset-password/" + idlink + "/"'''
            '''
            print("==================")
            print(body)

            body = MIMEText(body, _subtype='html')
            html_part.attach(body)

            email = EmailMessage(
                'CAMBIO DE CONTRASEÑA',
                None,
                settings.EMAIL_HOST_USER,
                [request.data['email']]
            )   
            email.attach(html_part)
            email.send()
            data = {
                'message': 'llave creada con exito, revisar el correo' 
            }
            return Response(data)

        except Exception as e:
            message = "Error"
            return Response({"error": False, "find": False, "message": str(e)})




        

class PasswordResetView(APIView):
    serializer_class = PasswordReset
    def post(self,request):
        serializer = PasswordReset(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'Clave cambiada' 
        }
        return Response(data)

#========== CRUD para la informacion basica del usuario ==========
#Listar todos los usuarios basicos
class UserList(ListAPIView):
    queryset = CustomUser.objects.all()
    #queryset = Worker.objects.all()
    serializer_class = UserSerializer
    #spermission_classes = (AllowOperator,)

#Crear un usuario
class UserCreate(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


#Listar un usuario por id
class UserDetail(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

#Actualizar datos de un usuario por id
class UserUpdate(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

"""
#Eliminar usuario
class DeleteUser(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
"""

#========== CRUD para la informacion del cliente completo ==========
class ClientList(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientAllSerializer

#Crear un cliente plano, (requiere id_user Basic de antemano)
class ClientCreate(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientAllSerializer

#Listar un cliente por id
class ClientDetail(RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientAllSerializer

class ClientUpdate(UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientAllSerializer


#========== CRUD para la informacion del cliente simple ==========
#Listar todos los clientes planos
class ClientSingleList(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

#Crear un cliente plano, (requiere id_user Basic de antemano)
class ClientSingleCreate(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

#Listar un cliente por id
class ClientSingleDetail(RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientSingleUpdate(UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


#========== CRUD para la informacion del trabajador completo ==========
#Listar todos los trabajadores
class WorkerList(ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

#Listar un cliente por id
class WorkerDetail(RetrieveAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

#Crear un trabajador para asignar a usuario existente
class WorkerCreate(ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class WorkerUpdate(UpdateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


#========== CRUD para la informacion del trabajador single ==========
#Listar todos los trabajadores
class WorkerSingleList(ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSingleSerializer

#Listar un cliente por id
class WorkerSingleDetail(RetrieveAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSingleSerializer

#Crear un trabajador para asignar a usuario existente
class CreateSingleWorker(ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSingleSerializer

class WorkerSingleUpdate(UpdateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSingleSerializer

#Crear cliente incluyendo usuario al mismo tiempo
class NewClientCreate(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
