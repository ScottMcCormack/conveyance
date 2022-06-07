.. _api:

Developer Interface
===================

.. module:: conveyance

Conveyance
----------

.. autoclass:: conveyance.Conveyance
    :members: calculate_iso_method, resistance_secondary, resistance_concentrated

Conveyor Resistances
--------------------

.. autofunction:: conveyance.conveyor_resistances.resistance_main
.. autofunction:: conveyance.conveyor_resistances.resistance_gravity
.. autofunction:: conveyance.conveyor_resistances.resistance_inertial_friction
.. autofunction:: conveyance.conveyor_resistances.resistance_material_acceleration
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_wrap
.. autofunction:: conveyance.conveyor_resistances.resistance_material_skirtplates
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_cleaners
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_sag_tension
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_wrap_iso
.. autofunction:: conveyance.conveyor_resistances.tension_transmit_min

Belt Capacity
-------------

.. autofunction:: conveyance.belt_capacity.mass_density_material
.. autofunction:: conveyance.belt_capacity.mass_density_idler
.. autofunction:: conveyance.belt_capacity.volume_carried_material
.. autofunction:: conveyance.belt_capacity.volumetric_flow
.. autofunction:: conveyance.belt_capacity.belt_cs_area

Power Requirements
------------------

.. autofunction:: conveyance.power_requirements.power_requirements_motor
