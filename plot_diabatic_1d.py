import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl



def multiplot(data , labels, x_range, title=None, factor=False, range_y=(-1, 1), ylabel='Energy [eV]'):

    if factor:
        factor_h_to_ev = 27.2116
        for i, dat in enumerate(data):
            data[i] = factor_h_to_ev * np.array(dat)

    f = plt.figure(1)

    plt.title(title)
    for dat, label in zip(data, labels):
        plt.plot(x_range, dat, label=label)

    plt.xlim(3.5, 6.0)
    plt.ylim(*range_y)
    plt.legend()
    plt.xlabel('Distance X [Å]')
    plt.ylabel(ylabel)

    plt.show()
    return f


folder = '1d_plot/'

with open('data_1d.pkl', 'rb') as input:
    calculation_data = pickle.load(input)
    print('Loaded data from calculation_data.pkl')


total_data = []
d_coordinate = []
for distance in calculation_data['distance']:
        print('{}'.format(distance))
        if '{}'.format(distance) in calculation_data:
            data = calculation_data['{}'.format(distance)]
            total_data.append(data)
            d_coordinate.append(distance)

########################### W_DC ############################

data_1 = [data['diabatic_contributions']['W_DC'][0] for data in total_data]
data_2 = [data['diabatic_contributions']['W_DC'][1] for data in total_data]

f = multiplot([data_1, data_2], ['W_DC_1', 'W_DC_2'], d_coordinate, title='W_DC')
f.savefig(folder + "W_DC.pdf", bbox_inches='tight')

wdc1 = np.array(data_1)
wdc2 = np.array(data_2)

########################### W_CT ############################

data_1 = [data['diabatic_contributions']['W_CT'][0] for data in total_data]
data_2 = [data['diabatic_contributions']['W_CT'][1] for data in total_data]

f = multiplot([data_1, data_2], ['W_CT_1', 'W_CT_2'], d_coordinate, title='W_CT')
f.savefig(folder + "W_CT.pdf", bbox_inches='tight')

wct1 = np.array(data_1)
wct2 = np.array(data_2)

########################### W_e ############################

data_1 = [data['diabatic_contributions']['W_e'][0] for data in total_data]
data_2 = [data['diabatic_contributions']['W_e'][1] for data in total_data]

f = multiplot([data_1, data_2], ['W_e_1', 'W_e_2'], d_coordinate, title='W_e')
f.savefig(folder + "W_e.pdf", bbox_inches='tight')

we1 = np.array(data_1)
we2 = np.array(data_2)

########################### W_h ############################

data_1 = [data['diabatic_contributions']['W_h'][0] for data in total_data]
data_2 = [data['diabatic_contributions']['W_h'][1] for data in total_data]

f = multiplot([data_1, data_2], ['W_h_1', 'W_h_2'], d_coordinate, title='W_h')
f.savefig(folder + "W_h.pdf", bbox_inches='tight')

wh1 = np.array(data_1)
wh2 = np.array(data_2)

###################################### W per state ###########################

f = multiplot([wh1, we1, wct1, wdc1], ['W_h', 'W_e', 'W_CT', 'W_DC'], d_coordinate, title='State 1')
f.savefig(folder + "W_1.pdf", bbox_inches='tight')

f = multiplot([wh2, we2, wct2, wdc2], ['W_h', 'W_e', 'W_CT', 'W_DC'], d_coordinate, title='State 2')
f.savefig(folder + "W_2.pdf", bbox_inches='tight')


###################################### lambda ###########################

data_1 = [data['lambda'][0] for data in total_data]
data_2 = [data['lambda'][1] for data in total_data]

#data_1 = []
#for i, e in enumerate(np.array([data['lambda'] for data in total_data]).T[0]):
#    data_1.append(e)

#data_2 = []
#for i, e in enumerate(np.array([data['lambda'] for data in total_data]).T[1]):
#    data_2.append(e)

f = multiplot([data_1, data_2], ['lambda 1', 'lambda 2'], d_coordinate, range_y=[0, 0.6], ylabel='', title='lambda')
f.savefig(folder + "lambda.pdf", bbox_inches='tight')

l1 = np.array(data_1)
l2 = np.array(data_2)

f = multiplot([np.square(data_1), np.square(data_2)], ['lambda^2 1', 'lambda^2 2'], d_coordinate, range_y=[0, 0.6], ylabel='', title='lambda^2')
f.savefig(folder + "lambda2.pdf", bbox_inches='tight')

########################## E1 (Superexchange) ###########################

data_1 = 2 * l1 * np.sqrt(1 - l1**2) * (we1 + wh1)
data_2 = 2 * l2 * np.sqrt(1 - l2**2) * (we2 + wh2)

f = multiplot([data_1, data_2], ['E1-1', 'E1-2'], d_coordinate)
f.savefig(folder + "E1(superexchange).pdf", bbox_inches='tight')
e_11 = np.array(data_1)
e_12 = np.array(data_2)


#######################  diabatic_energies  ######################

data_1 = [np.average(data['diabatic_energies']['E_LE']) for data in total_data]
data_2 = [np.average(data['diabatic_energies']['E_CT']) for data in total_data]

e_le = np.array(data_1)
e_ct = np.array(data_2)

f = multiplot([data_1, data_2], ['E_LE', 'E_CT'], d_coordinate, title='Diabatic energies', range_y=[6, 13])
f.savefig(folder + "diabatic_energies.pdf", bbox_inches='tight')

#######################  Second order term  (E2)  #####################

data_1 = l1**2 * (e_ct - e_le + wct1 - wdc1)
data_2 = l2**2 * (e_ct - e_le + wct2 - wdc2)

f = multiplot([data_1, data_2], ['E2-1', 'E2-2'], d_coordinate)
f.savefig(folder + "E2.pdf", bbox_inches='tight')

e_21 = np.array(data_1)
e_22 = np.array(data_2)


###################### Diabatic energies ##################

data_1 = [data['diabatic_energies']['V_DC'] for data in total_data]
data_2 = [data['diabatic_energies']['V_CT'] for data in total_data]
data_3 = [data['diabatic_energies']['V_e'][0] for data in total_data]
data_4 = [data['diabatic_energies']['V_h'][0] for data in total_data]
data_5 = [data['diabatic_energies']['V_e'][1] for data in total_data]
data_6 = [data['diabatic_energies']['V_h'][1] for data in total_data]

f = multiplot([data_1, data_2,  data_3,  data_4,  data_5, data_6],
              ['V_DC', "V_CT", "V_e", "V_h", "V_e'", "V_h'"],
              d_coordinate, title='Diabatic energies')

f.savefig(folder + "diabatic_energies.pdf", bbox_inches='tight')

###################### Adiabatic energies ##################

data_1 = [data['adiabatic_energies']['E_1'] for data in total_data]
data_2 = [data['adiabatic_energies']['E_2'] for data in total_data]
data_3 = [data['adiabatic_energies']['E_3'] for data in total_data]
data_4 = [data['adiabatic_energies']['E_4'] for data in total_data]

f = multiplot([data_1, data_2,  data_3,  data_4,],
              ['state_1', 'state_2', 'state_3', 'state_4'],
              d_coordinate, title='Adiabatic energies', range_y=[6, 13])

f.savefig(folder + "adiabatic_energies.pdf", bbox_inches='tight')




