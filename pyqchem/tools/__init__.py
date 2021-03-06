import numpy as np
from pyqchem.units import DEBYE_TO_AU
import matplotlib.pyplot as plt
from pyqchem.plots import plot_configuration
import requests as req
from json import dumps


def print_excited_states(parsed_data, include_conf_rasci=False, include_mulliken_rasci=False):
    for i, state in enumerate(parsed_data):
        print('\nState {}'.format(i+1))
        if 'multiplicity' in state:
            print('Multiplicity', state['multiplicity'])

        if state['transition_moment'] is not None:
            print('Osc. strength: {:6.4f}'.format(state['oscillator_strength']))
            print('Transition DM: ', '{:6.4f} {:6.4f} {:6.4f}'.format(*state['transition_moment']),
                  ' ', state['dipole_moment_units'])

        print('Energy: ', state['excitation_energy'], ' ', state['excitation_energy_units'])

        if include_conf_rasci:
            print('    Configurations')
            print('  Hole   Alpha  Beta   Part   Amplitude')
            for j, conf in enumerate(state['configurations']):
                print(' {:^6} {:^6} {:^6} {:^6} {:8.3f}'.format(conf['hole'], conf['alpha'], conf['beta'], conf['part'], conf['amplitude']))

        if include_mulliken_rasci:
            print('Mulliken analysis')
            print('         Attach    Detach    Total ')
            for i_atom, (at, det) in enumerate(zip(state['mulliken']['attach'],
                                                   state['mulliken']['detach'])):
                print('{:5}  {:8.4f}  {:8.4f}  {:8.4f}'.format(i_atom + 1, at, det, at + det))




def plot_rasci_state_configurations(states):
    for i, state in enumerate(states):
        plt.figure(figsize=(len(state['configurations']), 5))
        plt.title('State {}'.format(i+1))
        amplitude_list = []
        for j, conf in enumerate(state['configurations']):
            plot_configuration(conf['alpha'], conf['beta'], index=j)
            amplitude_list.append(conf['amplitude'])

        plt.plot(range(1, len(amplitude_list)+1), np.square(amplitude_list)*len(state['configurations'][0]['alpha']), label='amplitudes')
        plt.xlabel('Configurations')
        plt.ylabel('Amplitude')
        plt.axis('off')
        plt.legend()

    plt.show()


def submit_notice(message, service='pushbullet', pb_token=None, sp_url=None):
    """
    Submit a notification using webhooks

    :param message: The message to send
    :param service: pushbullet or samepage
    :param pb_token: pushbullet token
    :param sp_url: samepage url
    :return:
    """

    if service.lower() == 'pushbullet':
        url = 'https://api.pushbullet.com/v2/pushes'
        bot_message = {'body': message, 'type': 'note'}
        message_headers = {'Content-Type': 'application/json; charset=UTF-8',
                           'Access-Token': pb_token}
    elif service.lower() == 'samepage':
        url = sp_url
        bot_message = {'text': message}
        message_headers = {'Content-Type': 'application/json'}
    else:
        print('client not found!')
        return

    r = req.post(url=url,
                 headers=message_headers,
                 data=dumps(bot_message))

    r.close()


def rotate_coordinates(coordinates, angle, axis, atoms_list=None):
    """
    Rotate the coordinates (or range of coordinates) with respect a given axis

    :param coordinates: coordinates to rotate
    :param angle: rotation angle
    :param axis: rotation axis
    :param atoms_list: list of atoms to rotate (if None then rotate all)
    :return: rotated coordinates
    """
    coordinates = np.array(coordinates)

    cos_term = 1 - np.cos(angle)
    rot_matrix = [[axis[0]**2*cos_term + np.cos(angle), axis[0]*axis[1]*cos_term - axis[2]*np.sin(angle), axis[0]*axis[2]*cos_term + axis[1]*np.sin(angle)],
                  [axis[1]*axis[0]*cos_term + axis[2]*np.sin(angle), axis[1]**2*cos_term + np.cos(angle), axis[1]*axis[2]*cos_term + axis[0]*np.sin(angle)],
                  [axis[2]*axis[0]*cos_term + axis[1]*np.sin(angle), axis[1]*axis[2]*cos_term + axis[0]*np.sin(angle), axis[2]**2*cos_term + np.cos(angle)]]

    if atoms_list is not None:
        coordinates[atoms_list] = np.dot(coordinates[atoms_list], rot_matrix)
    else:
        coordinates = np.dot(coordinates, rot_matrix)

    return coordinates.tolist()
