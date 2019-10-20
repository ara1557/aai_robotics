#!/usr/bin/python
####################################################
# REALIZA O CONTROLE DO UR5 PARA TOCAR NO CAVALETE #
####################################################

import rospy
from rosi_defy.msg import ManipulatorJoints
from geometry_msgs.msg import TwistStamped, Pose
from math import pi, sqrt
from tf.transformations import euler_from_quaternion

class RosiNodeClass():

    def __init__(self):
        # Variaveis que controlam a rotina de toque
        self.touch = 0
        self.state = 0

        # Variavel que alerta sobre a forca
        self.forceFlag = 0
        
        # Comandos a serem enviados para as juntas
        self.joint1 = 0.0
        self.joint2 = 0.0
        self.joint3 = 0.0
        self.joint4 = 0.0
        self.joint5 = 0.0
        self.joint6 = 0.0

        # Posicao desejada das juntas
        self.desired_joint1 = 0.0
        self.desired_joint2 = 0.0
        self.desired_joint3 = 0.0
        self.desired_joint4 = 0.0
        self.desired_joint5 = 0.0
        self.desired_joint6 = 0.0

        # Publica em jointsPosTargetCommand
        self.pub_jointsPos = rospy.Publisher('/ur5/jointsPosTargetCommand',  ManipulatorJoints, queue_size=1)

        self.subpinto = rospy.Subscriber('/aai_rosi_pose', Pose, self.callback_pose)

        # Subscreve em jointsPositionCurrentState, forceTorqueSensorOutput e aai_rosi_pose
        self.sub_joints = rospy.Subscriber('/ur5/jointsPositionCurrentState', ManipulatorJoints, self.callback_joints)
        self.sub_force = rospy.Subscriber('/ur5/forceTorqueSensorOutput', TwistStamped, self.callback_force)

        # Define a frequencia de publicacao
        node_sleep_rate = rospy.Rate(10)

        # Loop principal do algoritmo
        while not rospy.is_shutdown():
            #
            traj = ManipulatorJoints()
            traj.header.stamp = rospy.Time.now()
            traj.joint_variable = [self.joint1, self.joint2, self.joint3, self.joint4, self.joint5, self.joint6]

            # Publica a mensagem
            self.pub_jointsPos.publish(traj)

            # Pausa
            node_sleep_rate.sleep()


    # Funcao de callback do sensor de forca
    def callback_pose(self, data):
		q_x = data.orientation.x
		q_y = data.orientation.y
		q_z = data.orientation.z
		q_w = data.orientation.w
		# Orientacao de quaternios para angulos de Euler
		euler_angles = euler_from_quaternion([q_x, q_y, q_z, q_w])

		self.pos_x  = data.position.x
		self.pos_y = data.position.y
		self.angle = euler_angles[2] # Apenas o angulo de Euler no eixo z nos interessa

    def callback_force(self, data):
        # Calculo e analise da forca
        force = sqrt(data.twist.linear.x**2 + data.twist.linear.y**2 + data.twist.linear.z**2)
        if force >= 1.5:
            print('forceFlag!!')
            self.forceFlag = 1
        else:
            self.forceFlag = 0

    # Funcao de callback das juntas
    def callback_joints(self, data):
        # Erro permitido
        self.err = 0.05

        # Posicao atual das juntas
        self.actual1 = data.joint_variable[0]
        self.actual2 = data.joint_variable[1]
        self.actual3 = data.joint_variable[2]
        self.actual4 = data.joint_variable[3]
        self.actual5 = data.joint_variable[4]
        self.actual6 = data.joint_variable[5]
        
        # Checa se o toque já ocorreu
        if(self.forceFlag == 1):
            self.touch = 1

        # No ponto especifico inicia a rotina
        #if(abs(self.pos_x - 0) >= self.err and abs(self.pos_y - 0) >= self.err and abs(self.angle - 0) >= self.err and self.touch != 1):
        
        if(abs(self.actual1 - pi/2) <= self.err and abs(self.actual5 + pi/2) <= self.err and self.state == 0):
            self.state = 1
            print(self.state)
        elif(abs(self.actual2 + pi/3) <= self.err and abs(self.actual4 - pi/3) <= self.err and self.state == 1):
            self.state = 2
            print(self.state)
        elif(abs(self.actual3 - pi/3) <= self.err and abs(self.actual4 - 0) <= self.err and self.state == 2):
            self.state = 3
            print(self.state)
        elif(abs(self.actual2 - 0) <= self.err and abs(self.actual4 + pi/3) <= self.err and self.state == 3):
            self.state = 4
            print(self.state)

        if(self.state == 0):
            print('estado 0')
            self.desired_joint1 = pi/2
            self.desired_joint2 = 0.0
            self.desired_joint3 = 0.0
            self.desired_joint4 = 0.0
            self.desired_joint5 = -pi/2
            self.desired_joint6 = 0.0
        if(self.state == 1):
            print('estado 1')
            self.desired_joint1 = self.joint1
            self.desired_joint2 = -pi/3
            self.desired_joint3 = self.joint3
            self.desired_joint4 = pi/3
            self.desired_joint5 = self.joint5
            self.desired_joint6 = self.joint6
        if(self.state == 2):
            print('estado 2')
            self.desired_joint1 = self.joint1
            self.desired_joint2 = self.joint2
            self.desired_joint3 = pi/3
            self.desired_joint4 = 0.0
            self.desired_joint5 = self.joint5
            self.desired_joint6 = self.joint6
        if(self.state == 3):
            print('estado 3')
            self.desired_joint1 = self.joint1
            self.desired_joint2 = 0.0
            self.desired_joint3 = self.joint3
            self.desired_joint4 = -pi/3
            self.desired_joint5 = self.joint5
            self.desired_joint6 = self.joint6
        if(self.state == 4):
            print('estado 4')
            self.desired_joint1 = self.joint1
            self.desired_joint2 = pi/2
            self.desired_joint3 = self.joint3
            self.desired_joint4 = -5*pi/6
            self.desired_joint5 = self.joint5
            self.desired_joint6 = self.joint6
        
        # Volta as juntas para a posicao inicial
        if(self.touch == 1):
            print('estado 5')
            self.state = 5
            self.desired_joint2 = 0.0
            if(abs(self.actual2 - 0) <= self.err):
                self.desired_joint3 = 0.0
                self.desired_joint4 = 0.0
            if(abs(self.actual3 - 0) <= self.err and abs(self.actual4 - 0) <= self.err):
                self.desired_joint1 = 0.0
                self.desired_joint5 = 0.0


        self.joint1 = self.desired_joint1
        self.joint2 = self.desired_joint2
        self.joint3 = self.desired_joint3
        self.joint4 = self.desired_joint4
        self.joint5 = self.desired_joint5
        self.joint6 = self.desired_joint6


if __name__ == '__main__':

    # Inicializa o no
    rospy.init_node('rosi_touch_control', anonymous=True)

    # Inicializa o objeto
    try:
        node_obj = RosiNodeClass()
    except rospy.ROSInterruptException:
        pass
