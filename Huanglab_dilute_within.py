from opentrons import containers, instruments
'''
Create a new container
'''
containers.create(
    'Epptubes',                    # name of you container
    grid=(3,4),                    # specify amount of (columns, rows)
    spacing=(13, 13),               # distances (mm) between each (column, row)
    diameter=8,                     # diameter (mm) of each well on the plate
    depth=40)                       # depth (mm) of each well on the plate)



# source of diluent
tuberack = containers.load('Epptubes', 'D3')
#plate_96 = containers.load('96-PCR-flat', 'B1')
pcr_strip_d1 = containers.load('PCR-strip-tall', 'B1')
#pcr_strip_d2 = containers.load('PCR-strip-tall', 'B1')

#Qpcr_strip = containers.load('opentrons-aluminum-block-PCR-strips-200ul', 'C1')
tiprack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('trash-box', 'C2')

#diluent_source = trough['A1']


# HACK: need to explicitly load each container like this
# instead of using a for loop, so that deck map can be parsed out
# for protocol library

# plate dilution will happen in
# plate_slots = ['A1', 'B1', 'A2', 'B2', 'A3', 'B3']

# plates = [c o n t a i n e r s.load(
#     '96-PCR-flat', slot) for slot in plate_slots]


# tip rack for p200 pipette
# tiprack_slots = ['C1', 'C3', 'D1', 'D3', 'E1', 'E2', 'E3']

# tipracks = [c o n t a i n e r s.load(
#     'tiprack-200ul', slot) for slot in tiprack_slots]

    #containers.load('tiprack-200ul', 'E3')

# trash location


p100_test = instruments.Pipette(
    trash_container=trash,
    tip_racks=[tiprack],
    min_volume=10,
    max_volume=100,
    axis="b",
)



def run_simple_protocol(dilution_factor: 10.0, final_volume: 100):
    '''
    dilute the original dye solution 10x and 100x, distribute in two PCR strips
    '''
    transfer_vol = final_volume/dilution_factor
    diluent_vol = final_volume - transfer_vol
    distribute_vol = (final_volume-10)/8
    '''
    Step1: create a secondary dilusion
    A1: original dye solution
    B2: water (or other solvent)
    B1: secondary dye solution (10x)
    C1: secondary dye solution (100x)
    '''

    p100_test.transfer(
        transfer_vol,
        tuberack.wells('A1'),
        tuberack.wells('B1'))

    p100_test.transfer(
        diluent_vol,
        tuberack.wells('B2'),
        tuberack.wells('B1'),
        mix_after = (5, diluent_vol/2))

    p100_test.transfer(
        transfer_vol,
        tuberack.wells('B1'),
        tuberack.wells('C1'))

    p100_test.transfer(
        diluent_vol,
        tuberack.wells('B2'),
        tuberack.wells('C1'),
        mix_after = (5, diluent_vol/2))



    p100_test.distribute(
        distribute_vol,
        tuberack.wells('C1'),
        pcr_strip_d1.rows('1')
    )

    p100_test.distribute(
        distribute_vol,
        tuberack.wells('C1'),
        pcr_strip_d1.rows('3')
    )

    #p200_test.transfer(diluent_vol)



run_simple_protocol(**{'dilution_factor': 10.0, 'final_volume': 200.0})
