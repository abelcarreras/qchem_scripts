__author__ = 'Abel Carreras'
from pyqchem.utils import search_bars


def _get_orbital_energies(orbitals_section):
    occupied = orbitals_section.find('-- Occupied --')
    virtual = orbitals_section.find('-- Virtual --')

    occupied_section = orbitals_section[occupied:virtual]
    virtual_section = orbitals_section[virtual:]

    occupied_energies = [float(energy) for energy in occupied_section.split()[3:]]
    virtual_energies = [float(energy) for energy in virtual_section.split()[3:]]

    return {'occupied': occupied_energies, 'virtual': virtual_energies}


def basic_parser_qchem(output):

    data_dict = {}

    # scf energy
    enum = output.find('Total energy in the final basis set')
    data_dict['scf_energy'] = float(output[enum:enum+100].split()[8])

    # Orbitals energy
    enum = output.find('Orbital Energies (a.u.)')
    bars = search_bars(output, from_position=enum, bar_type='----')
    orbitals_section = output[enum:bars[1]]

    alpha_mos = orbitals_section.find('Alpha MOs')
    beta_mos = orbitals_section.find('Beta MOs')

    if beta_mos > 0:
        alpha_energies = _get_orbital_energies(orbitals_section[alpha_mos:beta_mos])
        beta_energies = _get_orbital_energies(orbitals_section[beta_mos:])
    else:
        alpha_energies = _get_orbital_energies(orbitals_section[alpha_mos:])
        beta_energies = alpha_energies

    data_dict['orbital_energies'] = {'alpha': alpha_energies, 'beta': beta_energies, 'units': 'au'}

    # Mulliken Net Atomic Charges
    enum = output.find('Ground-State Mulliken Net Atomic Charges')
    bars = search_bars(output, from_position=enum, bar_type='----')
    mulliken_section = output[bars[0]:bars[1]]
    data_dict['mulliken_charges'] = [float(line.split()[2]) for line in mulliken_section.split('\n')[1:-1]]

    # Multipole Moments
    enum = output.find('Cartesian Multipole Moments')
    bars = search_bars(output, from_position=enum, bar_type='----')
    multipole_section = output[bars[0]: bars[1]]
    multipole_lines =  multipole_section.split('\n')[1:-1]

    multipole_dict = {}

    multipole_dict['charge'] = float(multipole_lines[1])
    multipole_dict['charge_units'] = 'ESU x 10^10'

    multipole_dict['dipole_moment'] = [float(val) for val in multipole_lines[3].split()[1::2]]
    multipole_dict['dipole_units'] = 'Debye'

    multipole_dict['quadrupole_moment'] = [float(val) for val in multipole_lines[6].split()[1::2]] + \
                                          [float(val) for val in multipole_lines[7].split()[1::2]]
    multipole_dict['quadrupole_units'] = 'Debye-Ang'

    multipole_dict['octopole_moment'] = [float(val) for val in multipole_lines[9].split()[1::2]] + \
                                        [float(val) for val in multipole_lines[10].split()[1::2]] + \
                                        [float(val) for val in multipole_lines[11].split()[1::2]] + \
                                        [float(val) for val in multipole_lines[12].split()[1::2]]
    multipole_dict['octopole_units'] = 'Debye-Ang^2'

    data_dict['multipole'] = multipole_dict

    return data_dict


