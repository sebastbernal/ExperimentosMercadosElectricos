##Se importan las librerias
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Sebastián Bernal García & Nelson Felipe Barco'

doc = """
Your app description
"""


##Esta clase contiene las constantes del juego, estas seran aplicadas a todas las sesiones
class Constants(BaseConstants):
    name_in_url = 'mercadoElectrico'
    players_per_group = 5
    num_rounds = 70
    instructions_template = 'mercadoElectrico/Instruction.html'


class Subsession(BaseSubsession):
    capacidadInstaladaTotalFinal = models.FloatField()
    precioFinal = models.FloatField()


##Esta clase tiene las variables que son grupales como el precio y la capacidad instalada total y los metodos para hacer
##Calculos que afectan a todo el grupo
class Group(BaseGroup):
    capacidadInstaladaTotal = models.FloatField(initial=0)
    precio = models.FloatField(initial=0)
    costo = models.FloatField(initial=1)

##Se hace el calculo de todos los participantes del grupo (su capacidad total instalada y en construccion) y
## posteriormente se calcula el precio (variable de grupo) y con este el margen de utilidad, la utilidad y el payoff
## para cada ronda
    def calculosGrupo(self):
        group = self
        players = group.get_players()
        for p in players:
            p.calculosParticipante()
        contributions = [p.CapacidadInstaladaActual for p in players]
        group.capacidadInstaladaTotal = sum(contributions)
        group.precio = 6 - (0.1 * group.capacidadInstaladaTotal)
        if group.precio < 0:
            group.precio = 0
        for p in players:
            p.calculoGanancia()
            p.calculoPayoff()
        return group.precio

##Este metodo realiza los calculos que se muestran al iniciar cada ronda, por que oTree resetea las variables al saltar
## de una ronda a otra
    def calculosIniciales(self):
        group = self
        players = group.get_players()
        for p in players:
            p.capacidadesPasadas()
            p.calculosTotales()
            p.lastRound = p.round_number - 1
            p.actualRound = p.round_number
        contributions = [p.CapacidadInstaladaActual for p in players]
        group.capacidadInstaladaTotal = sum(contributions)
        group.precio = 6 - (0.1 * group.capacidadInstaladaTotal)
        if group.precio < 0:
            group.precio = 0
        for p in players:
            p.calculoGanancia()
        return group.precio

##Clase jugador, es una instancia por cada participante. Aqui estan algunas variables que representan los dato
##Personales como son el nombre y el numero de cedula, y otras variables que son propias del juego como son 16 capacidades
##instaladas, 4 capacidades en construccion y la decision. Ademas tambien estan los metodos de la clase utilizados para
##Calcular la información de interes para el participante en particular como son el total de capacidades, la depreciacion
##de la instalacion y eviolucion de la construccion, calculo de la ganacia (utilidad) y el payoff
class Player(BasePlayer):
    ##Información personal del usuario
    nombre = models.StringField(
        label="Nombre",
    )
    cedula = models.IntegerField(
        label="No. Cedula",
        min=100000,
        max=999999999999,
    )
    cedulaDe = models.StringField(
        label="De (municipio)",
    )
    lastRound = models.IntegerField()
    actualRound = models.IntegerField()

    ##Información del juego
    ##Información de la inversion en nueva capacidad en construcción
    inversion = models.FloatField(
        min=0.0,
        max=55.0,
        initial=0,
    )
    ##Información de capacidad instalada
    capacidadInstalada1 = models.FloatField(initial=0.6875)
    capacidadInstalada2 = models.FloatField(initial=0.6875)
    capacidadInstalada3 = models.FloatField(initial=0.6875)
    capacidadInstalada4 = models.FloatField(initial=0.6875)
    capacidadInstalada5 = models.FloatField(initial=0.6875)
    capacidadInstalada6 = models.FloatField(initial=0.6875)
    capacidadInstalada7 = models.FloatField(initial=0.6875)
    capacidadInstalada8 = models.FloatField(initial=0.6875)
    capacidadInstalada9 = models.FloatField(initial=0.6875)
    capacidadInstalada10 = models.FloatField(initial=0.6875)
    capacidadInstalada11 = models.FloatField(initial=0.6875)
    capacidadInstalada12 = models.FloatField(initial=0.6875)
    capacidadInstalada13 = models.FloatField(initial=0.6875)
    capacidadInstalada14 = models.FloatField(initial=0.6875)
    capacidadInstalada15 = models.FloatField(initial=0.6875)
    capacidadInstalada16 = models.FloatField(initial=0.6875)

    ##Información de capacidad en construcción
    capacidadConstruida1 = models.FloatField(initial=0.6875)
    capacidadConstruida2 = models.FloatField(initial=0.6875)
    capacidadConstruida3 = models.FloatField(initial=0.6875)
    capacidadConstruida4 = models.FloatField(initial=0.6875)

    ##Información general de historicos
    CapacidadInstaladaActual = models.FloatField(initial=0, max=55.0, )
    CapacidadConstruccionActual = models.FloatField(initial=0)
    utilidadAcumulada = models.FloatField(initial=0)
    utilidad = models.FloatField(initial=0)
    margenUtilidad = models.FloatField(initial=0)
    gananciaPeriodoAnterior = models.FloatField(initial=0)
    capacidadInstaladaOtrosJugadores = models.FloatField(initial=0)

    def calculosParticipante(self):
        player = self
        group = self.group

        ##Si la ronda es la primera, no existe una ronda cero, por tanto ser toman los datos de la misma ronda
        if self.round_number == 1:
            ##Calculo capacidadaes instaladas al cambiar de año (ronda)
            player.capacidadInstalada16 = player.in_round(self.round_number).capacidadInstalada15
            player.capacidadInstalada15 = player.in_round(self.round_number).capacidadInstalada14
            player.capacidadInstalada14 = player.in_round(self.round_number).capacidadInstalada13
            player.capacidadInstalada13 = player.in_round(self.round_number).capacidadInstalada12
            player.capacidadInstalada12 = player.in_round(self.round_number).capacidadInstalada11
            player.capacidadInstalada11 = player.in_round(self.round_number).capacidadInstalada10
            player.capacidadInstalada10 = player.in_round(self.round_number).capacidadInstalada9
            player.capacidadInstalada9 = player.in_round(self.round_number).capacidadInstalada8
            player.capacidadInstalada8 = player.in_round(self.round_number).capacidadInstalada7
            player.capacidadInstalada7 = player.in_round(self.round_number).capacidadInstalada6
            player.capacidadInstalada6 = player.in_round(self.round_number).capacidadInstalada5
            player.capacidadInstalada5 = player.in_round(self.round_number).capacidadInstalada4
            player.capacidadInstalada4 = player.in_round(self.round_number).capacidadInstalada3
            player.capacidadInstalada3 = player.in_round(self.round_number).capacidadInstalada2
            player.capacidadInstalada2 = player.in_round(self.round_number).capacidadInstalada1
            player.capacidadInstalada1 = player.in_round(self.round_number).capacidadConstruida4

            ##Calculo capacidadaes en construccion al cambiar de año (ronda)
            player.capacidadConstruida4 = player.in_round(self.round_number).capacidadConstruida3
            player.capacidadConstruida3 = player.in_round(self.round_number).capacidadConstruida2
            player.capacidadConstruida2 = player.in_round(self.round_number).capacidadConstruida1
            player.capacidadConstruida1 = player.in_round(self.round_number).inversion

            player.calculosTotales()
        ##Der lo contrario se toman los datros de la ronda pasada.
        else:
            ##Calculo capacidadaes instaladas al cambiar de año (ronda)
            player.capacidadInstalada16 = player.in_round(self.round_number - 1).capacidadInstalada15
            player.capacidadInstalada15 = player.in_round(self.round_number - 1).capacidadInstalada14
            player.capacidadInstalada14 = player.in_round(self.round_number - 1).capacidadInstalada13
            player.capacidadInstalada13 = player.in_round(self.round_number - 1).capacidadInstalada12
            player.capacidadInstalada12 = player.in_round(self.round_number - 1).capacidadInstalada11
            player.capacidadInstalada11 = player.in_round(self.round_number - 1).capacidadInstalada10
            player.capacidadInstalada10 = player.in_round(self.round_number - 1).capacidadInstalada9
            player.capacidadInstalada9 = player.in_round(self.round_number - 1).capacidadInstalada8
            player.capacidadInstalada8 = player.in_round(self.round_number - 1).capacidadInstalada7
            player.capacidadInstalada7 = player.in_round(self.round_number - 1).capacidadInstalada6
            player.capacidadInstalada6 = player.in_round(self.round_number - 1).capacidadInstalada5
            player.capacidadInstalada5 = player.in_round(self.round_number - 1).capacidadInstalada4
            player.capacidadInstalada4 = player.in_round(self.round_number - 1).capacidadInstalada3
            player.capacidadInstalada3 = player.in_round(self.round_number - 1).capacidadInstalada2
            player.capacidadInstalada2 = player.in_round(self.round_number - 1).capacidadInstalada1
            player.capacidadInstalada1 = player.in_round(self.round_number - 1).capacidadConstruida4

            ##Calculo capacidadaes en construccion al cambiar de año (ronda)
            player.capacidadConstruida4 = player.in_round(self.round_number - 1).capacidadConstruida3
            player.capacidadConstruida3 = player.in_round(self.round_number - 1).capacidadConstruida2
            player.capacidadConstruida2 = player.in_round(self.round_number - 1).capacidadConstruida1
            player.capacidadConstruida1 = player.in_round(self.round_number).inversion

            player.calculosTotales()

    def calculosTotales(self):
        player = self
        group = self.group

        ##Capacidad instalada total de cad aparticipante
        player.CapacidadInstaladaActual = (
                player.capacidadInstalada1 + player.capacidadInstalada2 + player.capacidadInstalada3 +
                player.capacidadInstalada4 + player.capacidadInstalada5 + player.capacidadInstalada6 +
                player.capacidadInstalada7 +
                player.capacidadInstalada8 + player.capacidadInstalada9 + player.capacidadInstalada10 +
                player.capacidadInstalada11 + player.capacidadInstalada12 + player.capacidadInstalada13 +
                player.capacidadInstalada14 + player.capacidadInstalada15 + player.capacidadInstalada16)

        ##Capacidad construccion total de cad aparticipante
        player.CapacidadConstruccionActual = (player.capacidadConstruida1 + player.capacidadConstruida2 +
                                              player.capacidadConstruida3 + player.capacidadConstruida4)

    ##Calculo capacidades de la ronda pasada para mostrar al iniciar la ronda, esto por que oTree resetea topdas las
    ##variables al iniciar cada ronda
    def capacidadesPasadas(self):
        player = self
        group = self.group
        ##Solo aplica si ronda es superiro a la primera, en la primera no exidte capacidades pasadas
        if self.round_number != 1:
            ##Calculo capacidadaes instaladas al cambiar de año (ronda)
            player.capacidadInstalada16 = player.in_round(self.round_number - 1).capacidadInstalada16
            player.capacidadInstalada15 = player.in_round(self.round_number - 1).capacidadInstalada15
            player.capacidadInstalada14 = player.in_round(self.round_number - 1).capacidadInstalada14
            player.capacidadInstalada13 = player.in_round(self.round_number - 1).capacidadInstalada13
            player.capacidadInstalada12 = player.in_round(self.round_number - 1).capacidadInstalada12
            player.capacidadInstalada11 = player.in_round(self.round_number - 1).capacidadInstalada11
            player.capacidadInstalada10 = player.in_round(self.round_number - 1).capacidadInstalada10
            player.capacidadInstalada9 = player.in_round(self.round_number - 1).capacidadInstalada9
            player.capacidadInstalada8 = player.in_round(self.round_number - 1).capacidadInstalada8
            player.capacidadInstalada7 = player.in_round(self.round_number - 1).capacidadInstalada7
            player.capacidadInstalada6 = player.in_round(self.round_number - 1).capacidadInstalada6
            player.capacidadInstalada5 = player.in_round(self.round_number - 1).capacidadInstalada5
            player.capacidadInstalada4 = player.in_round(self.round_number - 1).capacidadInstalada4
            player.capacidadInstalada3 = player.in_round(self.round_number - 1).capacidadInstalada3
            player.capacidadInstalada2 = player.in_round(self.round_number - 1).capacidadInstalada2
            player.capacidadInstalada1 = player.in_round(self.round_number - 1).capacidadInstalada1

            ##Calculo capacidadaes en construccion al cambiar de año (ronda)
            player.capacidadConstruida4 = player.in_round(self.round_number - 1).capacidadConstruida4
            player.capacidadConstruida3 = player.in_round(self.round_number - 1).capacidadConstruida3
            player.capacidadConstruida2 = player.in_round(self.round_number - 1).capacidadConstruida2
            player.capacidadConstruida1 = player.in_round(self.round_number - 1).capacidadConstruida1

            player.CapacidadInstaladaActual = player.in_round(self.round_number - 1).CapacidadInstaladaActual

            player.CapacidadConstruccionActual = player.in_round(self.round_number - 1).CapacidadConstruccionActual

    ##Se calcula la ganancia para cada participante en base al precio grupal, el costo y el margen de utilidad.
    def calculoGanancia(self):
        player = self
        group = self.group
        player.margenUtilidad = group.precio - group.costo
        player.utilidad = player.CapacidadInstaladaActual * player.margenUtilidad
        if self.round_number == 1:
            player.utilidadAcumulada = player.utilidad
        else:
            player.utilidadAcumulada = player.in_round(self.round_number - 1).utilidadAcumulada + player.utilidad
        player.capacidadInstaladaOtrosJugadores = group.capacidadInstaladaTotal - player.CapacidadInstaladaActual

    ##Se calcula el pago en el mundo real, payoff, para cada participante en base a su utilidad acumulada
    def calculoPayoff(self):
        player = self
        group = self.group
        if player.utilidadAcumulada <= -300:
            self.participant.payoff = c(0)
            print('Entre a ganancia de menor a -300')
        elif player.utilidadAcumulada > 300:
            self.participant.payoff = c(45000).to_real_world_currency(self.session)
            print('Entre a ganancia de mayor a 300')
        else:
            self.participant.payoff = c((abs(-300 - player.utilidadAcumulada) * 75)).to_real_world_currency(
                self.session)
            print('Entre a ganancia intermedia')
        print(player.utilidadAcumulada)
