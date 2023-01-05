# The standard way to import NumPy:
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import mean as meanFunction
from matplotlib.lines import Line2D
from scipy.integrate import nquad
import io
import base64
import urllib


# In these calculas we consider that the collision occurs at the origin of the inertial coordinate system

# Final position of the center of mass of the vehicle 1 in the inertial coordinate system
FINAL_POS_1 = np.array([99.924, -49.409])
# Final position of the center of mass of the vehicle 2 in the inertial coordinate system
FINAL_POS_2 = np.array([99.1, -52.253])

# Pre-impact position of the center of mass of the vehicle 1 in the inertial coordinate system
PRE_IMPACT_POS_1 = np.array([100.311, -48.906])
# Pre-impact position of the center of mass of the vehicle 2 in the inertial coordinate system
PRE_IMPACT_POS_2 = np.array([97.755, -49,912])

def compute_init_speeds(m1, m2, v1f, v2f, theta1, theta2, theta1f, theta2f):
    """
    Computes the initial speeds of the two vehicles in a head-on collision.
    
    m1: mass of the vehicle 1
    m2: mass of the vehicle 2
    v1f: speed of the vehicle 1 at the instant of separation
    v2f: speed of the vehicle 2 at the instant of separation
    theta1: angle of the pre-impact velocity vector of vehicle 1
    theta2: angle of the pre-impact velocity vector of vehicle 2
    theta1f: angle of the separation velocity vector of vehicle 1
    theta2f: angle of the separation velocity vector of vehicle 2
    """
    c1 = m1 * v1f * np.cos(np.radians(theta1f)) + m2 * v2f * np.cos(np.radians(theta2f))
    c2 = m1 * v1f * np.sin(np.radians(theta1f)) + m2 * v2f * np.sin(np.radians(theta2f))
    
    
    return (np.cos(np.radians(theta2)) * c2 - c1 * np.sin(np.radians(theta2))) / (m1 * np.sin(np.radians(theta1 - theta2))), \
            (np.cos(np.radians(theta1)) * c2 - c1 * np.sin(np.radians(theta1))) / (m2 * np.sin(np.radians(theta2 - theta1)))        
    

def compute_angular_speed(delta_psi, mu, I, m, L, f, d):
    """ 
    Computes the angular speed of the vehicle
    
    delta_psi: total vehicle yaw angle in the post-impact configuration
    mu: coefficient of friction
    I: moment of inertia of the vehicle
    m: mass of the vehicle
    L: wheelbase of the vehicle
    f: coefficient of rolling resistance
    d: distance between the center of mass in the pre-impact configuration and the center of mass in the final configuration
    """
    
    return np.sign(delta_psi) * np.sqrt((mu * 9.81 * np.square(delta_psi)) / ((I/ m*L) * (1-f) * np.abs(delta_psi) + d/1.7))

def compute_separation_velocity(mu, delta_psi, omega, I, m, L, f):
    """
    Computes the separation velocity of the vehicle
    
    mu: coefficient of friction
    delta_psi: total vehicle yaw angle in the post-impact configuration
    omega: angular speed of the vehicle
    I: moment of inertia of the vehicle
    m: mass of the vehicle
    L: wheelbase of the vehicle
    f: coefficient of rolling resistance
    """
    
    return 1.7 * ((mu * 9.81 * delta_psi / omega) - (I / (m * L)) * (1 - f) * omega)

def get_abs_distance(p1, p2):
    """
    Returns the absolute distance between two points
    
    p1: first point
    p2: second point
    """
    
    return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))

def get_ees(m1, m2, v1, v2, v1f, v2f):
    """
    Returns the energy equivalent speed of the collision
    
    m1: mass of the vehicle 1
    m2: mass of the vehicle 2
    v1: speed of the vehicle 1
    v2: speed of the vehicle 2
    v1f: speed of the vehicle 1 at the instant of separation
    v2f: speed of the vehicle 2 at the instant of separation
    """
    
    Ed = (0.5 * m1 * np.square(v1) + 0.5 * m2 * np.square(v2)) - (0.5 * m1 * np.square(v1f) + 0.5 * m2 * np.square(v2f))
    EES2 = np.sqrt(Ed / m2)
    return np.sqrt(m2/m1) * EES2, EES2

def get_results(d1, d2, m1Base, m1Delta, m2Base, m2Delta, theta1Base, theta1Delta, theta2Base, theta2Delta, theta1fBase, theta1fDelta, theta2fBase, theta2fDelta, n, a1Base, a1Delta, a2Base, a2Delta):
    # Array used to store all the results of the monte carlo simulation
    resultsV1 = []
    resultsV2 = []
    resultEES1 = []
    resultEES2 = []
    
    # Define the distance from impact to final positions
    d1 = d1
    d2 = d2
    
    # Define EES values for each vehicle
    EES1Base = 27.0
    EES1Delta = 5.0
    
    EES2Base = 30.0
    EES2Delta = 5.0
    
    
    for i in range(n):
        # Pick uniformly parameters for the Monte Carlo simulation
        m1 = random.uniform(m1Base - m1Delta, m1Base + m1Delta)
        m2 = random.uniform(m2Base - m2Delta, m2Base + m2Delta)
        
        theta1 = random.uniform(theta1Base - theta1Delta, theta1Base + theta1Delta)
        theta2 = random.uniform(theta2Base - theta2Delta, theta2Base + theta2Delta)
        
        theta1f = random.uniform(theta1fBase - theta1fDelta, theta1fBase + theta1fDelta)
        theta2f = random.uniform(theta2fBase - theta2fDelta, theta2fBase + theta2fDelta)
        
        a1 = random.uniform(a1Base - a1Delta, a1Base + a1Delta)
        a2 = random.uniform(a2Base - a2Delta, a2Base + a2Delta)
        
        v1s = np.sqrt(2 * a1 * d1) * 3.6
        v2s = np.sqrt(2 * a2 * d2) * 3.6
        
        v1, v2 = compute_init_speeds(m1, m2, v1s, v2s, theta1, theta2, theta1f, theta2f)
        
        EES1, EES2 = get_ees(m1, m2, v1, v2, v1s, v2s)
        resultEES1.append(EES1)
        resultEES2.append(EES2)
        
        resultsV1.append(round(v1, 1))
        resultsV2.append(round(v2, 1))
    
    print(meanFunction(resultEES1))
    print(meanFunction(resultEES2))
    
    plt.figure()
    sns.kdeplot(resultsV1, fill=True, label=' Probability density function')
    plt.xlabel('Initial speed of vehicle 1 (km/h)')
    plt.title('Probability density function of the initial speed of vehicle 1')
    mean = meanFunction(resultsV1)
    plt.axvline(mean, linestyle='dashed', color='r', linewidth=2)
    legend_entry = Line2D([0], [0], color='r', linestyle='dashed', label=f'mean = {mean:.2f}')
    plt.legend(handles=[legend_entry])

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri1 = urllib.parse.quote(string)
    

    
    # plt2 = plt.figure()
    # sns.kdeplot(resultEES1, fill=True, label=' Probability density function')
    # plt2.xlabel('EES of vehicle 1')
    # plt2.title('Probability density function of the EES of vehicle 1')
    # plt2.axvline(mean, linestyle='dashed', color='r', linewidth=2)
    # legend_entry = Line2D([0], [0], color='r', linestyle='dashed', label=f'mean = {mean:.2f}')
    # plt2.legend(handles=[legend_entry])
    
    
    plt.figure()
    sns.kdeplot(resultsV2, fill=True, label=' Probability density function')
    plt.xlabel('Initial speed of vehicle 1 (km/h)')
    plt.title('Probability density function of the initial speed of vehicle 2')
    mean = meanFunction(resultsV2)
    plt.axvline(mean, linestyle='dashed', color='r', linewidth=2)
    legend_entry = Line2D([0], [0], color='r', linestyle='dashed', label=f'mean = {mean:.2f}')
    plt.legend(handles=[legend_entry])

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri2 = urllib.parse.quote(string)
    
    plt.figure()
    kdeplot = sns.kdeplot(x=resultsV1, y=resultsV2, fill=True, cmap='Reds', cbar=True,)
    plt.xlabel('Initial speed of vehicle 1 (km/h)')
    plt.ylabel('Initial speed of vehicle 2 (km/h)')
    plt.title('Bivariate probability density function of the initial speed of the vehicles')


    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri3 = urllib.parse.quote(string)


    return uri1, uri2, uri3

