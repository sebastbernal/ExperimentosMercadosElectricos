##Se importan librerias
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

##El juego esta compuesto por varias fases como es el consentimiento, la introduccion, las instrucciones, la pagina
##de inverison y de resultados. Cada una de estas clases representa respectivamente ca una de las paginas

##PAgina de introduccion
class Introduction(Page):
    form_model = 'player'
##metodo que asegura que la introduccion solo se muestre en la ronda 1
    def is_displayed(self):
        return self.round_number == 1
        return True

##PAgoina de firma de consentimiento
class Consentimiento(Page):
    form_model = 'player'
    ##campos del formulario que se pasara al fronted
    form_fields = ['nombre', 'cedula', 'cedulaDe']

##Metodo para validar los campos del formulario que sean el formato y estructura aceptado
    def error_message(self, values):
        print('values is', values)
        a = [k for k in values['nombre'] if k.isdigit()]
        if a:
            return 'El nombre debe ser una cadena de caracteres sin numeros'

        if type(values['cedula']) != int:
            return 'La cedula solo debe contener numeros'

        b = [k for k in values['cedulaDe'] if k.isdigit()]
        if b:
            return 'El municipio debe ser una cadena de caracteres sin numeros'
        if values['cedula'] > 999999999999:
            return 'La cedula no puede exeder los 12 caracteres/numeros'

    ##metodo que asegura que el consentimiento solo se muestre en la ronda 1
    def is_displayed(self):
        return self.round_number == 1
        return True

##Pagina inical de instrucciones
class Instrucciones2(Page):
    form_model = 'player'
##metodo que asegura que las instrucciones solas, solo se muestre en la ronda 1
    def is_displayed(self):
        return self.round_number == 1
        return True

##PAgina de invsersion donde se toma la desicion de cuanto invertir en nuyeva capacidad instalada
class Inversion(Page):

    form_model = 'player'
    ##Campo del formulario
    form_fields = ['inversion']

    ##metodo que asegura el calculo del estado del grupo y cada uno de los jugadores al principio de cada ronda para
    ##mostrarlo en la pagina de inversion
    def is_displayed(self):
        self.group.calculosIniciales()
        return True

    ##Este metodo pasa las variables para graficar el comportamiento del prcio y la capacidad instalada total del mercado
    ##En el tiempo (ronda)
    def vars_for_template(self):
        precio = []
        años = []
        instaladaTotal=[]
        for g in self.group.in_rounds(1, self.group.round_number-1):
            precio.append(g.precio)
            instaladaTotal.append(g.capacidadInstaladaTotal)
            años.append(g.round_number)
        return dict(
            precio=precio,
            años = años,
            instaladaTotal = instaladaTotal,
        )

    ##Este metdoo evita que la capacidad total del participante supere las 20 unidades al tomar la decision de la
    ##inversion.
    def error_message(self, values):
        print('values is', values)
        total= values['inversion'] + self.player.CapacidadConstruccionActual +self.player.CapacidadInstaladaActual
        resto = 20 - self.player.CapacidadConstruccionActual - self.player.CapacidadInstaladaActual
        print(total)
        if total > 20:
            return ('Tu capacidad instalada y construida no puede superar las 20 unidades. Tu maxima inversion es de' , resto,' unidades.')

##PAgina de espera despues de tomar la desicion de inversion, para esperar a que todos los participantes lleguen alli
class Results2WaitPage(WaitPage):
    title_text = 'Espera de resultados'
    body_text = 'Esperando que todos los jugadores realicen su inversión...'
    ##metodo que se dispara cuando todos los participantes llegan al la pagina de espera depsues de tomar la desicion y
    ##llama al metodo de grupo para el calculo de las variables de grupo
    def after_all_players_arrive(self):
        self.group.calculosGrupo()

class consentimientoWaitPage(WaitPage):
    title_text = 'Espera la firma de consentimiento de todos los jugadores'
    body_text = 'Esperando que todos los jugadores esten listos...'
    def is_displayed(self):
        return self.round_number == 1
        return True
    def after_all_players_arrive(self):
        #self.player.calculosTotales()
        #self.group.calculosIniciales()
        return True



class Results2(Page):
    form_model = 'player'

    #def vars_for_template(self):
    #    precio = []
    #    años = []
    #    for g in self.group.in_all_rounds():
    #        precio.append(g.precio)
    #        años.append(g.round_number)
    #        print(precio)
    #        print(años)
    #    return dict(
    #        precio=precio,
    #        años = años,
    #    )

page_sequence = [
    Introduction,
    #Consentimiento,
    #consentimientoWaitPage,
    Instrucciones2,
    Inversion,
    Results2WaitPage,
    Results2,
]
